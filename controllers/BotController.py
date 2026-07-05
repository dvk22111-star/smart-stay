from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.dependencies import get_db
from dtos import BotSessionDTO, BotSessionCreateDTO, BotAnswerCreateDTO
from services.mapper.BotSession import bot_session_service
from services.mapper.BotAnswer import bot_answer_service
from services.mapper.BotProcessor import bot_processor_service
from models import (
    BotAnswer,
    BotRegistrationSession,
    BotSessionStatusEnum,
    User,
    Group,
    Preferences,
    RoomPreferences,
    Room,
    Vacation,
)
from services.repository.user_repository import UserRepository
from services.repository.group_repository import GroupRepository
from services.repository.group_members_repository import GroupMembersRepository
from bot.flow import next_question, get_question, handle_answer
from bot.validation import is_valid_email
from bot.parser import parse_yes_no, detect_inquiry

router = APIRouter(prefix="/bot", tags=["Bot"])


@router.post("/sessions", response_model=BotSessionDTO)
def create_session(payload: BotSessionCreateDTO, db: Session = Depends(get_db)):
    try:
        return bot_session_service.create(db, payload)
    except IntegrityError as e:
        db.rollback()
        if "FOREIGN KEY constraint failed" in str(e):
            raise HTTPException(
                status_code=400,
                detail="Invalid VacationID or GroupID. Please check that the vacation and group exist."
            )
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")


@router.get("/sessions/{session_id}", response_model=BotSessionDTO)
def get_session(session_id: int, db: Session = Depends(get_db)):
    return bot_session_service.get_by_id(db, session_id)


@router.get("/sessions/{session_id}/current-question")
def get_current_question(session_id: int, db: Session = Depends(get_db)):
    session = bot_session_service.get_by_id(db, session_id)
    return {
        "current_question": get_question(session.CurrentQuestionID) if session.CurrentQuestionID else None,
        "session": session,
    }


@router.post("/sessions/{session_id}/verify-phone")
def verify_phone(session_id: int, db: Session = Depends(get_db)):
    session = bot_session_service.get_by_id(db, session_id)
    user = UserRepository(db).get_by_phone(session.Phone)

    session.Status = BotSessionStatusEnum.IN_PROGRESS
    if user:
        session.UserID = user.UserID
        session.CurrentQuestionID = session.CurrentQuestionID or "QUESTION_INTRO"
    else:
        session.CurrentQuestionID = "QUESTION_NAME"

    bot_session_service.update_current_question(db, session_id, session.CurrentQuestionID)

    group = None
    group_name = None
    has_group_discount = False
    if user and user.UserID:
        members = GroupMembersRepository(db).get_by_telephone(session.Phone)
        if members:
            group = GroupRepository(db).get_by_id(members[0].GroupID)
        else:
            groups = GroupRepository(db).get_by_user_id(user.UserID)
            if groups:
                group = groups[0]

        group_name = group.GroupName if group else None
        has_group_discount = bool(group and group.PaidAsAGroup)

    db.commit()
    db.refresh(session)

    if user:
        greeting = f"שלום {user.Name}, שמחתי להכיר! את שייכת לקבוצה {group_name if group_name else 'פרטית'}."
    else:
        greeting = "שלום, לא מצאתי את מספר הטלפון שלך במערכת. נתחיל רישום חדש."

    response = {
        "message": greeting,
        "group_name": group_name,
        "has_group_discount": has_group_discount,
        "session": session,
        "next_question": get_question(session.CurrentQuestionID),
    }
    return response


@router.post("/sessions/{session_id}/answers")
def add_answer(session_id: int, payload: BotAnswerCreateDTO, db: Session = Depends(get_db)):
    session = bot_session_service.get_by_id(db, session_id)
    if session.Status != BotSessionStatusEnum.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Session is not in progress")

    question_id = payload.QuestionID or session.CurrentQuestionID or "QUESTION_INTRO"
    answer = BotAnswer(
        SessionID=session.SessionID,
        QuestionID=question_id,
        AnswerText=payload.AnswerText,
        IsFinal=str(payload.IsFinal).lower(),
    )

    parse_result = handle_answer(question_id, payload.AnswerText)
    parsed_value = parse_result.get("parsed")

    # Detect generic inquiries (dates/location/maternity refunds) and answer immediately
    inquiry = detect_inquiry(payload.AnswerText)
    if inquiry:
        if inquiry == "unrelated":
            saved_answer = bot_answer_service.create(db, answer)
            session.CurrentQuestionID = session.CurrentQuestionID or "QUESTION_INTRO"
            bot_session_service.update_current_question(db, session_id, session.CurrentQuestionID)
            return {
                "inquiry": "unrelated",
                "message": "אני עונה רק על שאלות הקשורות לנופש והרשמה. כדי לסיים את הרישום, אנא התמקד/י בשאלות הנדרשות להשלמת התהליך.",
                "next_question": get_question(session.CurrentQuestionID) if session.CurrentQuestionID else None,
                "session": {
                    "SessionID": session.SessionID,
                    "UserID": session.UserID,
                    "VacationID": session.VacationID,
                    "GroupID": session.GroupID,
                    "Phone": session.Phone,
                    "Status": session.Status.value if hasattr(session.Status, 'value') else session.Status,
                    "CurrentQuestionID": session.CurrentQuestionID,
                },
            }

        if inquiry == "maternity":
            return {
                "inquiry": "maternity",
                "message": "יש לנו החזרי לידה אך הדבר צריך להיות מסודר מול המלון ולא דרכנו.",
                "next_question": get_question(session.CurrentQuestionID),
                "session": session,
            }

        if inquiry in ("dates", "location"):
            if not session.VacationID:
                return {
                    "inquiry": inquiry,
                    "message": "אין מידע על חופשה משויך למשתמש זה.",
                    "next_question": get_question(session.CurrentQuestionID),
                    "session": session,
                }
            try:
                from models import Vacation
                vac = db.query(Vacation).filter(Vacation.VacationID == session.VacationID).first()
                if not vac:
                    return {
                        "inquiry": inquiry,
                        "message": "לא נמצא מידע על החופשה.",
                        "next_question": get_question(session.CurrentQuestionID),
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
                        "next_question": get_question(session.CurrentQuestionID),
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
                            "next_question": get_question(session.CurrentQuestionID),
                            "session": session,
                        }
                    return {
                        "inquiry": "location",
                        "message": "אין מידע על המלון המשויך לחופשה.",
                        "next_question": get_question(session.CurrentQuestionID),
                        "session": session,
                    }
            except Exception:
                return {
                    "inquiry": inquiry,
                    "message": "שגיאה בשליפת מידע על החופשה.",
                    "next_question": get_question(session.CurrentQuestionID),
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

    if parsed_value is not None:
        answer.set_parsed_value(parsed_value)

    saved_answer = bot_answer_service.create(db, answer)

    if parsed_value is not None:
        bot_processor_service.process_answer(db, session, question_id, parsed_value)
    next_q = parse_result.get("next_question") or next_question(question_id)
    if isinstance(next_q, dict):
        next_question_id = next_q["id"]
    else:
        next_question_id = next_q

    session.CurrentQuestionID = next_question_id
    bot_session_service.update_current_question(db, session_id, session.CurrentQuestionID)

    return {
        "answer": {
            "AnswerID": saved_answer.AnswerID,
            "SessionID": saved_answer.SessionID,
            "QuestionID": saved_answer.QuestionID,
            "AnswerText": saved_answer.AnswerText,
            "ParsedValue": saved_answer.get_parsed_value(),
            "IsFinal": saved_answer.IsFinal,
            "CreatedAt": saved_answer.CreatedAt,
        },
        "next_question": get_question(session.CurrentQuestionID) if session.CurrentQuestionID else None,
        "session": {
            "SessionID": session.SessionID,
            "UserID": session.UserID,
            "VacationID": session.VacationID,
            "GroupID": session.GroupID,
            "Phone": session.Phone,
            "Status": session.Status.value if hasattr(session.Status, 'value') else session.Status,
            "CurrentQuestionID": session.CurrentQuestionID,
        },
    }


@router.post("/sessions/{session_id}/complete")
def complete_session(session_id: int, db: Session = Depends(get_db)):
    session = bot_session_service.update_status(db, session_id, "COMPLETED")
    return {"message": "Session completed", "session_id": session.SessionID}
