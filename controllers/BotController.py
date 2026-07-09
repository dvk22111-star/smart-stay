from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.dependencies import get_db
from dtos import BotSessionDTO, BotSessionCreateDTO, BotAnswerCreateDTO
from services.mapper.BotProcessor import bot_processor_service
from bot.temp_user_service import temp_user_service
from models import (
    User,
    Group,
    Preferences,
    RoomPreferences,
    Room,
    Vacation,
)
from types import SimpleNamespace
from datetime import datetime

# In-memory sessions store (bot-only, no DB tables)
SESSIONS: dict[int, dict] = {}
_NEXT_SESSION_ID = 1

class InMemoryStatus:
    AWAITING_VERIFICATION = "AWAITING_VERIFICATION"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
from services.repository.user_repository import UserRepository
from services.repository.group_repository import GroupRepository
from services.repository.group_members_repository import GroupMembersRepository
from bot.flow import next_question, get_question, handle_answer
from bot.validation import is_valid_email
from bot.parser import parse_yes_no, detect_inquiry

router = APIRouter(prefix="/bot", tags=["Bot"])


@router.post("/sessions", response_model=BotSessionDTO)
def create_session(payload: BotSessionCreateDTO, db: Session = Depends(get_db)):
    global _NEXT_SESSION_ID
    session_id = _NEXT_SESSION_ID
    _NEXT_SESSION_ID += 1

    now = datetime.utcnow()
    session = {
        "SessionID": session_id,
        "UserID": None,
        "VacationID": payload.VacationID,
        "GroupID": payload.GroupID,
        "Phone": payload.Phone,
        "Status": InMemoryStatus.AWAITING_VERIFICATION,
        "CurrentQuestionID": None,
        "CreatedAt": now,
        "UpdatedAt": now,
    }
    SESSIONS[session_id] = session
    temp_user_service.save(
    str(session_id),
    {
        "Phone": payload.Phone
    }
)
    return session


@router.get("/sessions/{session_id}", response_model=BotSessionDTO)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Bot session not found")
    return session


@router.get("/sessions/{session_id}/current-question")
def get_current_question(session_id: int, db: Session = Depends(get_db)):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Bot session not found")
    return {
        "current_question": get_question(session.get("CurrentQuestionID")) if session.get("CurrentQuestionID") else None,
        "session": session,
    }


@router.post("/sessions/{session_id}/verify-phone")
def verify_phone(session_id: int, db: Session = Depends(get_db)):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Bot session not found")

    user = UserRepository(db).get_by_phone(session["Phone"])

    session["Status"] = InMemoryStatus.IN_PROGRESS
    if user:
        session["UserID"] = user.UserID
        session["CurrentQuestionID"] = session.get("CurrentQuestionID") or "QUESTION_INTRO"
    else:
        session["CurrentQuestionID"] = "QUESTION_NAME"

    group = None
    group_name = None
    has_group_discount = False
    if user and user.UserID:
        members = GroupMembersRepository(db).get_by_telephone(session["Phone"])
        if members:
            group = GroupRepository(db).get_by_id(members[0].GroupID)
        else:
            groups = GroupRepository(db).get_by_user_id(user.UserID)
            if groups:
                group = groups[0]

        group_name = group.GroupName if group else None
        has_group_discount = bool(group and group.PaidAsAGroup)

    session["UpdatedAt"] = datetime.utcnow()

    if user:
        greeting = f"שלום {user.Name}, שמחתי להכיר! את שייכת לקבוצה {group_name if group_name else 'פרטית'}."
    else:
        greeting = "שלום, לא מצאתי את מספר הטלפון שלך במערכת. נתחיל רישום חדש."

    response = {
        "message": greeting,
        "group_name": group_name,
        "has_group_discount": has_group_discount,
        "session": session,
        "next_question": get_question(session.get("CurrentQuestionID")),
    }
    return response


@router.post("/sessions/{session_id}/answers")
def add_answer(session_id: int, payload: BotAnswerCreateDTO, db: Session = Depends(get_db)):
    print(SESSIONS)
    print(session_id)
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Bot session not found")
    if session.get("Status") != InMemoryStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Session is not in progress")

    question_id = payload.QuestionID or session.get("CurrentQuestionID") or "QUESTION_INTRO"

    parse_result = handle_answer(question_id, payload.AnswerText)
    parsed_value = parse_result.get("parsed")

    # Detect generic inquiries (dates/location/maternity refunds) and answer immediately
    inquiry = detect_inquiry(payload.AnswerText)
    if inquiry:
        if inquiry == "unrelated":
            session["CurrentQuestionID"] = session.get("CurrentQuestionID") or "QUESTION_INTRO"
            session["UpdatedAt"] = datetime.utcnow()
            return {
                "inquiry": "unrelated",
                "message": "אני עונה רק על שאלות הקשורות לנופש והרשמה. כדי לסיים את הרישום, אנא התמקד/י בשאלות הנדרשות להשלמת התהליך.",
                "next_question": get_question(session.get("CurrentQuestionID")) if session.get("CurrentQuestionID") else None,
                "session": session,
            }

        if inquiry == "maternity":
            return {
                "inquiry": "maternity",
                "message": "יש לנו החזרי לידה אך הדבר צריך להיות מסודר מול המלון ולא דרכנו.",
                "next_question": get_question(session.get("CurrentQuestionID")),
                "session": session,
            }

        if inquiry in ("dates", "location"):
            if not session.get("VacationID"):
                return {
                    "inquiry": inquiry,
                    "message": "אין מידע על חופשה משויך למשתמש זה.",
                    "next_question": get_question(session.get("CurrentQuestionID")),
                    "session": session,
                }
            try:
                from models import Vacation
                vac = db.query(Vacation).filter(Vacation.VacationID == session.get("VacationID")).first()
                if not vac:
                    return {
                        "inquiry": inquiry,
                        "message": "לא נמצא מידע על החופשה.",
                        "next_question": get_question(session.get("CurrentQuestionID")),
                        "session": session,
                    }

                if inquiry == "dates":
                    start = vac.StartV.isoformat() if getattr(vac, 'StartV', None) else None
                    end = vac.EndV.isoformat() if getattr(vac, 'EndV', None) else None
                    return {
                        "inquiry": "dates",
                        "start_date": start,
                        "end_date": end,
                        "message": f"תאריכי החופשה הם: {start} עד {end}.",
                        "next_question": get_question(session.get("CurrentQuestionID")),
                        "session": session,
                    }

                if inquiry == "location":
                    hotel = vac.hotel if getattr(vac, 'hotel', None) else None
                    if hotel:
                        return {
                            "inquiry": "location",
                            "hotel_name": hotel.Name,
                            "hotel_address": hotel.Address,
                            "message": f"החופשה ב\'{hotel.Name}\' - כתובת: {hotel.Address}.",
                            "next_question": get_question(session.get("CurrentQuestionID")),
                            "session": session,
                        }
                    return {
                        "inquiry": "location",
                        "message": "אין מידע על המלון המשויך לחופשה.",
                        "next_question": get_question(session.get("CurrentQuestionID")),
                        "session": session,
                    }
            except Exception:
                return {
                    "inquiry": inquiry,
                    "message": "שגיאה בשליפת מידע על החופשה.",
                    "next_question": get_question(session.get("CurrentQuestionID")),
                    "session": session,
                }

    if question_id == "QUESTION_EMAIL":
        if not parsed_value or not is_valid_email(parsed_value):
            raise HTTPException(status_code=400, detail="כתובת המייל לא תקינה, נסי שוב.")

    if question_id == "QUESTION_PREFERENCE_PRIORITY" and not parsed_value:
        raise HTTPException(status_code=400, detail="לא הצלחתי לזהות את הדירוג. כתבי למשל 'נוף לים 1'.")

    if question_id == "QUESTION_PARTNER_REQUEST":
        cleaned = payload.AnswerText.strip().lower()
        if cleaned and parsed_value is None and cleaned not in ("לא", "אין", "no", "none"):
            raise HTTPException(status_code=400, detail="אנא צייני מספר טלפון תקין של החברה, או כתבי 'לא' אם אין חברה.")

    # Persist parsed values into existing tables via processor
    if parsed_value is not None:
        # store answer in in-memory session for processor lookups
        answers = session.get('answers') or []
        answers.append({
            'QuestionID': question_id,
            'AnswerText': payload.AnswerText,
            'ParsedValue': parsed_value,
            'CreatedAt': datetime.utcnow(),
        })
        session['answers'] = answers
        session_obj = SimpleNamespace(**session)
        bot_processor_service.process_answer(db, session_obj, question_id, parsed_value)

    next_q = parse_result.get("next_question") or next_question(question_id)
    if isinstance(next_q, dict):
        next_question_id = next_q["id"]
    else:
        next_question_id = next_q

    session["CurrentQuestionID"] = next_question_id
    session["UpdatedAt"] = datetime.utcnow()

    return {
        "answer": None,
        "next_question": get_question(session.get("CurrentQuestionID")) if session.get("CurrentQuestionID") else None,
        "session": session,
    }


@router.post("/sessions/{session_id}/complete")
def complete_session(session_id: int, db: Session = Depends(get_db)):
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Bot session not found")
    session["Status"] = InMemoryStatus.COMPLETED
    session["UpdatedAt"] = datetime.utcnow()
    return {"message": "Session completed", "session_id": session["SessionID"]}
