from datetime import date
import json

from fastapi import HTTPException
from sqlalchemy.orm import Session
from types import SimpleNamespace

from models import (
    CustomerPreferences,
    Group,
    GroupMembers,
    Preferences,
    PreferenceTypeEnum,
    PartnerRequest,
    User,
    Vacation,
    VacationersCustomers,
    Room,
    RoomPreferences
)
from services.repository.customer_preferences_repository import CustomerPreferencesRepository
from services.repository.preferences_repository import PreferencesRepository
from services.repository.partner_request_repository import PartnerRequestRepository
from services.repository.user_repository import UserRepository
from bot.temp_user_service import temp_user_service

class BotProcessorService:
    def process_answer(self, db: Session, session, question_id: str, parsed_value):
        if question_id == "QUESTION_NAME":
            return self._process_name(db, session, parsed_value)
        if question_id == "QUESTION_EMAIL":
            return self._process_email(db, session, parsed_value)
        if question_id == "QUESTION_GROUP_TYPE":
            return self._process_group_type(db, session, parsed_value)
        if question_id == "QUESTION_GROUP_PAYMENT_TYPE":
            return self._process_group_payment_type(db, session, parsed_value)
        if question_id == "QUESTION_GROUP_MEMBER_PHONES":
            return self._process_group_member_phones(db, session, parsed_value)
        if question_id == "QUESTION_PREFERENCE_PRIORITY":
            return self._process_preference_priorities(db, session, parsed_value)
        if question_id == "QUESTION_PARTNER_REQUEST":
            return self._process_partner_request(db, session, parsed_value)
        if question_id == "QUESTION_CREDIT_AMOUNT":
            return self._process_credit_amount(db, session, parsed_value)
        return None

    def _get_latest_answer(self, session, question_id: str):
        # Look up latest answer in the in-memory session answers list (added by controller)
        answers = getattr(session, 'answers', None) or (session.get('answers') if isinstance(session, dict) else None)
        if answers:
            for a in reversed(answers):
                if a.get('QuestionID') == question_id:
                    return SimpleNamespace(ParsedValue=a.get('ParsedValue'), AnswerText=a.get('AnswerText'))
        return None


    def _ensure_vacation_customer(self, db: Session, user_id: int, vacation_id: int):
        existing = db.query(VacationersCustomers).filter(
            VacationersCustomers.UserID == user_id,
            VacationersCustomers.VacationID == vacation_id,
        ).first()
        if existing:
            return existing
        vc = VacationersCustomers(
            UserID=user_id,
            VacationID=vacation_id,
            UpdateDate=date.today(),
        )
        db.add(vc)
        db.commit()
        db.refresh(vc)
        return vc

    def _process_name(self, db, session, name):

        if not name or not name.strip():
            raise HTTPException(
                status_code=400,
                detail="אנא הכנס שם תקין"
            )

        temp_user_service.update(
            str(session.SessionID),
            "Name",
            name.strip()
     )

        return True
    def _process_email(self, db: Session, session, email: str):
        if not email:
           raise HTTPException(status_code=400, detail="כתובת המייל ריקה.")

        name_answer = self._get_latest_answer(
            session,
            "QUESTION_NAME",
    )

        name_text = None

        if name_answer:
            name_text = name_answer.ParsedValue or name_answer.AnswerText

        if not name_text or not name_text.strip():
            raise HTTPException(
                status_code=400,
                detail="לא נמצא שם משתמש תקין. אנא הזן שם קודם."
        )

        temp_user_service.update(
            str(session.SessionID),
            "Email",
             email.strip()
            )


        return temp_user_service.get(str(session.SessionID))
    def _process_group_type(self, db: Session, session, parsed_value):
        return parsed_value

    def _process_group_payment_type(self, db: Session, session, parsed_value):
        return parsed_value

    def _process_group_member_phones(self, db: Session, session, phone_list: list[str]):
        if not phone_list:
            raise HTTPException(status_code=400, detail="אנא ספק/י לפחות מספר טלפון אחד של חברי הקבוצה.")
        if not temp_user_service.get(str(session.SessionID)):
            raise HTTPException(
                status_code=400,
                detail="Session missing temporary user"
                )
           
        if not session.VacationID:
            raise HTTPException(status_code=400, detail="Session missing vacation information.")

        group_name_answer = self._get_latest_answer(session, "QUESTION_GROUP_NAME")
        group_size_answer = self._get_latest_answer(session,"QUESTION_GROUP_SIZE",)
        payment_answer = self._get_latest_answer( session, "QUESTION_GROUP_PAYMENT_TYPE",)
        group_name = (group_name_answer.ParsedValue or group_name_answer.AnswerText).strip() if group_name_answer else None
        group_size = int(group_size_answer.ParsedValue or group_size_answer.AnswerText) if group_size_answer else None
        paid_as_group = payment_answer.ParsedValue if payment_answer else False

        if not group_name:
            raise HTTPException(status_code=400, detail="אנא הזן שם קבוצה תקין.")
        if not group_size or group_size < 1:
            raise HTTPException(status_code=400, detail="אנא הזן מספר משתתפים תקין.")

        temp_user_service.update(
            str(session.SessionID),
            "Group",
            {
            "UserID": None,
            "GroupName": group_name,
            "NumberofParticipants": group_size,
            "VacationID": session.VacationID,
            "GroupPrice": 0.0,
            "IndividualPrice": 0.0,
            "PaidAsAGroup": bool(paid_as_group),
            "Members": phone_list
            }
        )
        return True

    def _process_preference_priorities(self, db: Session, session, priorities: dict):
        if not priorities:
            raise HTTPException(status_code=400, detail="לא זוהו העדפות תקינות.")
        if len(set(priorities.values())) != len(priorities.values()):
            raise HTTPException(status_code=400, detail="כל דירוג יכול להיבחר פעם אחת בלבד.")

       
        vacation_id = session.VacationID
        data = temp_user_service.get(str(session.SessionID))

        if not data or not vacation_id:
            raise HTTPException(
                status_code=400,
                detail="Session missing user or vacation information."
            )

        vacation = db.query(Vacation).filter(Vacation.VacationID == vacation_id).first()
        if not vacation:
            raise HTTPException(status_code=400, detail="Vacation not found.")

        
        for pref_key, rating in priorities.items():
            try:
                pref_type = PreferenceTypeEnum[pref_key]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"העדפה לא נתמכת: {pref_key}")

            preference = db.query(Preferences).filter(Preferences.PreferenceType == pref_type).first()
            if not preference:
                preference = Preferences(PreferenceType=pref_type)
                db.add(preference)
                db.commit()
                db.refresh(preference)

            room_count = db.query(Room).join(RoomPreferences, Room.RoomID == RoomPreferences.RoomID).filter(
                RoomPreferences.IDPreferences == preference.PreferencesID,
                Room.HotelID == vacation.HotelID,
            ).count()
            if room_count == 0:
                raise HTTPException(status_code=400, detail=f"אין חדרים זמינים עם ההעדפה {pref_key} עבור נופש זה.")
        temp_user_service.update(
            str(session.SessionID),
           "Preferences",
           priorities
        )

        return priorities    
    def _process_partner_request(self, db: Session, session, partner_phone: str):
        if partner_phone is None:
            return None

       
        data = temp_user_service.get(str(session.SessionID))
        vacation_id = session.VacationID

        if not data or not vacation_id:
            raise HTTPException(
                status_code=400,
                detail="Session missing user or vacation information."
            )
        temp_user_service.update(
            str(session.SessionID),
            "PartnerPhone",
             partner_phone
        )

        return partner_phone
       

    def _process_credit_amount(self, db: Session, session, amount: float):
        if amount is None:
            raise HTTPException(status_code=400, detail="אנא הכנס/י סכום אשראי תקין.")
        if not temp_user_service.get(str(session.SessionID)):
            raise HTTPException(status_code=400, detail="Session missing user information.")

        temp_user_service.update(
            str(session.SessionID),
            "Credit",
            amount
        )

        return temp_user_service.get(str(session.SessionID))
    def finalize_registration(self, db, session):
        bot_processor_service = BotProcessorService()
        data = temp_user_service.get(str(session.SessionID))
        if not data:
            raise HTTPException(
                status_code=400,
                detail="לא נמצאו נתוני הרשמה."
            )
        required_fields = ["Name", "Email", "Phone", "Credit"]

        missing_fields = [
        field for field in required_fields
        if field not in data or data[field] is None
    ]

        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"חסרים נתונים להשלמת ההרשמה: {', '.join(missing_fields)}"
            )
        user = User(
            Name=data["Name"],
            Email=data["Email"],
            Phone=data["Phone"],
            Credit=data["Credit"]
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        session.UserID = user.UserID

    # יצירת VacationCustomer
    # יצירת Group
    # יצירת Preferences
    # יצירת PartnerRequest
        return user
bot_processor_service = BotProcessorService()