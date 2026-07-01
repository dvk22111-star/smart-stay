from sqlalchemy.orm import Session
from models import Preferences


class PreferencesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Preferences).order_by(Preferences.PreferencesID).all()

    def get_by_id(self, preference_id: int):
        return self.db.query(Preferences).filter(Preferences.PreferencesID == preference_id).first()

    def search_by_text(self, text: str):
        return self.db.query(Preferences).filter(Preferences.PreferenceType.ilike(f"%{text}%")).all()

    def get_by_type(self, type_name: str):
        return self.db.query(Preferences).filter(Preferences.PreferenceType.ilike(f"%{type_name}%")).all()

    def create(self, preference: Preferences):
        self.db.add(preference)
        self.db.commit()
        self.db.refresh(preference)
        return preference

    def update(self, preference: Preferences):
        self.db.commit()
        self.db.refresh(preference)
        return preference

    def delete(self, preference: Preferences):
        self.db.delete(preference)
        self.db.commit()
        return True
