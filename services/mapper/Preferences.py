from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.Preferences import Preferences, PreferenceTypeEnum
from services.repository.preferences_repository import PreferencesRepository


class PreferencesService:
    def get_all_preferences(self, db: Session):
        return PreferencesRepository(db).get_all()

    def get_preference_by_id(self, db: Session, preference_id: int):
        preference = PreferencesRepository(db).get_by_id(preference_id)
        if not preference:
            raise HTTPException(status_code=404, detail="Preference not found")
        return preference

    def search_preferences(self, db: Session, text: str):
        return PreferencesRepository(db).search_by_text(text)

    def get_preferences_by_type(self, db: Session, type_name: str):
        return PreferencesRepository(db).get_by_type(type_name)

    def create_preference(self, db: Session, payload):
        try:
            pref_type = PreferenceTypeEnum[payload.PreferenceType]
        except (KeyError, AttributeError):
            pref_type = PreferenceTypeEnum(payload.PreferenceType)
        preference = Preferences(PreferenceType=pref_type)
        return PreferencesRepository(db).create(preference)

    def update_preference(self, db: Session, preference_id: int, payload):
        repo = PreferencesRepository(db)
        preference = repo.get_by_id(preference_id)
        if not preference:
            raise HTTPException(status_code=404, detail="Preference not found")
        if payload.PreferenceType is not None:
            try:
                preference.PreferenceType = PreferenceTypeEnum[payload.PreferenceType]
            except (KeyError, AttributeError):
                preference.PreferenceType = PreferenceTypeEnum(payload.PreferenceType)
        return repo.update(preference)

    def delete_preference(self, db: Session, preference_id: int):
        repo = PreferencesRepository(db)
        preference = repo.get_by_id(preference_id)
        if not preference:
            raise HTTPException(status_code=404, detail="Preference not found")
        repo.delete(preference)
        return {"deleted": True}


preferences_service = PreferencesService()
