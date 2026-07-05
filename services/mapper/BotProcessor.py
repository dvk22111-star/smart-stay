from datetime import date
import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import (
    BotAnswer,
    CustomerPreferences,
    Group,
    GroupMembers,
    Preferences,
    PreferenceTypeEnum,
    PartnerRequest,
    User,
    Vacation,
    VacationersCustomers,
)
from services.repository.customer_preferences_repository import CustomerPreferencesRepository
from services.repository.preferences_repository import PreferencesRepository
from services.repository.partner_request_repository import PartnerRequestRepository
from services.repository.user_repository import UserRepository


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

    def _get_latest_answer(self, db: Session, session_id: int, question_id: str):
        return db.query(BotAnswer).filter(
            BotAnswer.SessionID == session_id,
            BotAnswer.QuestionID == question_id,
        ).order_by(BotAnswer.CreatedAt.desc()).first()

    def _create_or_update_user(self, db: Session, session, name: str, email: str):
        user_repo = UserRepository(db)
        if session.UserID:
            user = user_repo.get_by_id(session.UserID)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user.Name = name or user.Name
            user.Email = email or user.Email
            return user_repo.update(user)

        existing_user = user_repo.get_by_phone(session.Phone)
        if existing_user:
            existing_user.Name = name or existing_user.Name
            existing_user.Email = email or existing_user.Email
            session.UserID = existing_user.UserID
            return user_repo.update(existing_user)

        user = User(Name=name, Email=email, Phone=session.Phone)
        db.add(user)
        db.commit()
        db.refresh(user)
        session.UserID = user.UserID
        return user

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

    def _process_name(self, db: Session, session, name: str):
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="אנא הכניס/י שם תקין.")
        if session.UserID:
            user = UserRepository(db).get_by_id(session.UserID)
            if user:
                user.Name = name.strip()
                return UserRepository(db).update(user)
        return None

    def _process_email(self, db: Session, session, email: str):
        if not email:
            raise HTTPException(status_code=400, detail="כתובת המייל ריקה.")

        name_answer = self._get_latest_answer(db, session.SessionID, "QUESTION_NAME")
        name_text = None
        if name_answer:
            name_text = name_answer.ParsedValue or name_answer.AnswerText
        if not name_text or not name_text.strip():
            raise HTTPException(status_code=400, detail="לא נמצא שם משתמש תקין. אנא הזין שם קודם.")

        user = self._create_or_update_user(db, session, name_text.strip(), email.strip())

        if session.VacationID:
            self._ensure_vacation_customer(db, user.UserID, session.VacationID)

        return user

    def _process_group_type(self, db: Session, session, parsed_value):
        return parsed_value

    def _process_group_payment_type(self, db: Session, session, parsed_value):
        return parsed_value

    def _process_group_member_phones(self, db: Session, session, phone_list: list[str]):
        if not phone_list:
            raise HTTPException(status_code=400, detail="אנא ספק/י לפחות מספר טלפון אחד של חברי הקבוצה.")
        if not session.UserID:
            raise HTTPException(status_code=400, detail="Session missing user information.")
        if not session.VacationID:
            raise HTTPException(status_code=400, detail="Session missing vacation information.")

        group_name_answer = self._get_latest_answer(db, session.SessionID, "QUESTION_GROUP_NAME")
        group_size_answer = self._get_latest_answer(db, session.SessionID, "QUESTION_GROUP_SIZE")
        payment_answer = self._get_latest_answer(db, session.SessionID, "QUESTION_GROUP_PAYMENT_TYPE")

        group_name = (group_name_answer.ParsedValue or group_name_answer.AnswerText).strip() if group_name_answer else None
        group_size = int(group_size_answer.ParsedValue or group_size_answer.AnswerText) if group_size_answer else None
        paid_as_group = payment_answer.ParsedValue if payment_answer else False

        if not group_name:
            raise HTTPException(status_code=400, detail="אנא הזן שם קבוצה תקין.")
        if not group_size or group_size < 1:
            raise HTTPException(status_code=400, detail="אנא הזן מספר משתתפים תקין.")

        group = None
        if session.GroupID:
            group = db.query(Group).filter(Group.GroupID == session.GroupID).first()

        if not group:
            group = Group(
                UserID=session.UserID,
                GroupName=group_name,
                NumberofParticipants=group_size,
                VacationID=session.VacationID,
                GroupPrice=0.0,
                IndividualPrice=0.0,
                PaidAsAGroup=bool(paid_as_group),
            )
            db.add(group)
            db.commit()
            db.refresh(group)
            session.GroupID = group.GroupID
        else:
            group.GroupName = group_name
            group.NumberofParticipants = group_size
            group.PaidAsAGroup = bool(paid_as_group)
            db.commit()
            db.refresh(group)

        for phone in phone_list:
            existing_member = db.query(GroupMembers).filter(
                GroupMembers.GroupID == group.GroupID,
                GroupMembers.Telephone == phone,
            ).first()
            if not existing_member:
                member = GroupMembers(GroupID=group.GroupID, Telephone=phone)
                db.add(member)
        db.commit()

        return group

    def _process_preference_priorities(self, db: Session, session, priorities: dict):
        if not priorities:
            raise HTTPException(status_code=400, detail="לא זוהו העדפות תקינות.")
        if len(set(priorities.values())) != len(priorities.values()):
            raise HTTPException(status_code=400, detail="כל דירוג יכול להיבחר פעם אחת בלבד.")

        user_id = session.UserID
        vacation_id = session.VacationID
        if not user_id or not vacation_id:
            raise HTTPException(status_code=400, detail="Session missing user or vacation information.")

        vacation = db.query(Vacation).filter(Vacation.VacationID == vacation_id).first()
        if not vacation:
            raise HTTPException(status_code=400, detail="Vacation not found.")

        saved_entries = []
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

            existing_pref = db.query(CustomerPreferences).filter(
                CustomerPreferences.UserID == user_id,
                CustomerPreferences.VacationID == vacation_id,
                CustomerPreferences.PreferencesID == preference.PreferencesID,
            ).first()

            total_selected = db.query(CustomerPreferences).filter(
                CustomerPreferences.VacationID == vacation_id,
                CustomerPreferences.PreferencesID == preference.PreferencesID,
            ).count()
            if existing_pref:
                total_selected -= 1

            if total_selected >= room_count:
                raise HTTPException(status_code=400, detail=f"כבר הושלמה הדרישה להזמנה זו עבור ההעדפה {pref_key}.")

            if existing_pref:
                existing_pref.Rating = rating
                db.commit()
                db.refresh(existing_pref)
                saved_entries.append(existing_pref)
            else:
                customer_pref = CustomerPreferences(
                    Rating=rating,
                    UserID=user_id,
                    PreferencesID=preference.PreferencesID,
                    VacationID=vacation_id,
                )
                db.add(customer_pref)
                db.commit()
                db.refresh(customer_pref)
                saved_entries.append(customer_pref)

        return saved_entries

    def _process_partner_request(self, db: Session, session, partner_phone: str):
        if partner_phone is None:
            return None

        user_id = session.UserID
        vacation_id = session.VacationID
        if not user_id or not vacation_id:
            raise HTTPException(status_code=400, detail="Session missing user or vacation information.")

        user_repo = UserRepository(db)
        partner_user = user_repo.get_by_phone(partner_phone)

        partner_request = PartnerRequest(
            UserIDMember1=user_id,
            UserIDMember2=partner_user.UserID if partner_user else None,
            VacationID=vacation_id,
        )
        db.add(partner_request)
        db.commit()
        db.refresh(partner_request)
        return partner_request

    def _process_credit_amount(self, db: Session, session, amount: float):
        if amount is None:
            raise HTTPException(status_code=400, detail="אנא הכנס/י סכום אשראי תקין.")
        if not session.UserID:
            raise HTTPException(status_code=400, detail="Session missing user information.")

        user = UserRepository(db).get_by_id(session.UserID)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.Credit = amount
        return UserRepository(db).update(user)


bot_processor_service = BotProcessorService()
