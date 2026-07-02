from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import CustomerPreferences, Preferences, PreferenceTypeEnum, PartnerRequest
from services.repository.customer_preferences_repository import CustomerPreferencesRepository
from services.repository.preferences_repository import PreferencesRepository
from services.repository.partner_request_repository import PartnerRequestRepository
from services.repository.user_repository import UserRepository


class BotProcessorService:
    def process_answer(self, db: Session, session, question_id: str, parsed_value):
        if question_id == "QUESTION_PREFERENCE_PRIORITY":
            return self._process_preference_priorities(db, session, parsed_value)
        if question_id == "QUESTION_SEA_VIEW_CONFIRM":
            return self._process_sea_view_confirm(db, session, parsed_value)
        if question_id == "QUESTION_PARTNER_REQUEST":
            return self._process_partner_request(db, session, parsed_value)
        if question_id == "QUESTION_EMAIL":
            return self._process_email(db, session, parsed_value)
        return None

    def _process_preference_priorities(self, db: Session, session, priorities: dict):
        if not priorities:
            raise HTTPException(status_code=400, detail="לא זוהו העדפות תקינות.")

        user_id = session.UserID
        vacation_id = session.VacationID
        if not user_id or not vacation_id:
            raise HTTPException(status_code=400, detail="Session missing user or vacation information.")

        pref_repo = PreferencesRepository(db)
        cp_repo = CustomerPreferencesRepository(db)

        saved_entries = []
        for pref_key, rating in priorities.items():
            try:
                pref_type = PreferenceTypeEnum[pref_key]
            except KeyError:
                continue

            preference = db.query(Preferences).filter(Preferences.PreferenceType == pref_type).first()
            if not preference:
                preference = Preferences(PreferenceType=pref_type)
                db.add(preference)
                db.commit()
                db.refresh(preference)

            existing = cp_repo.get_by_user_vacation_preference(user_id, vacation_id, preference.PreferencesID)
            if existing:
                existing.Rating = rating
                cp_repo.update(existing)
                saved_entries.append(existing)
            else:
                customer_pref = CustomerPreferences(
                    Rating=rating,
                    UserID=user_id,
                    PreferencesID=preference.PreferencesID,
                    VacationID=vacation_id,
                )
                saved_entries.append(cp_repo.create(customer_pref))

        return saved_entries

    def _process_sea_view_confirm(self, db: Session, session, accepted: bool):
        # If accepted, ensure SEA_VIEW preference exists for user/vacation and mark it; if declined, remove it
        user_id = session.UserID
        vacation_id = session.VacationID
        if not user_id or not vacation_id:
            raise HTTPException(status_code=400, detail="Session missing user or vacation information.")

        pref_repo = PreferencesRepository(db)
        cp_repo = CustomerPreferencesRepository(db)

        try:
            pref_type = PreferenceTypeEnum['SEA_VIEW']
        except KeyError:
            return None

        preference = db.query(Preferences).filter(Preferences.PreferenceType == pref_type).first()
        if not preference:
            preference = Preferences(PreferenceType=pref_type)
            db.add(preference)
            db.commit()
            db.refresh(preference)

        existing = cp_repo.get_by_user_vacation_preference(user_id, vacation_id, preference.PreferencesID)
        # determine surcharge amount from hotel_preferences if available,
        # fall back to 10% of Vacation.BasicCost when price isn't configured
        if accepted:
            if existing:
                existing.Rating = 1
                cp_repo.update(existing)
                return existing
            customer_pref = CustomerPreferences(
                Rating=1,
                UserID=user_id,
                PreferencesID=preference.PreferencesID,
                VacationID=vacation_id,
            )
            return cp_repo.create(customer_pref)
        else:
            if existing:
                cp_repo.delete(existing)
            return None

    def _process_partner_request(self, db: Session, session, partner_phone: str):
        if not partner_phone:
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
        return PartnerRequestRepository(db).create(partner_request)

    def _process_email(self, db: Session, session, email: str):
        if not email:
            raise HTTPException(status_code=400, detail="כתובת המייל ריקה.")

        user_repo = UserRepository(db)
        user = user_repo.get_by_id(session.UserID)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.Email = email
        return user_repo.update(user)



bot_processor_service = BotProcessorService()
