from sqlalchemy.orm import Session
from models import PreferencePrice


class PreferencePriceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(PreferencePrice).order_by(PreferencePrice.PreferencePriceID).all()

    def get_by_id(self, preference_price_id: int):
        return self.db.query(PreferencePrice).filter(PreferencePrice.PreferencePriceID == preference_price_id).first()

    def get_by_preference_id(self, preference_id: int):
        return self.db.query(PreferencePrice).filter(PreferencePrice.PreferenceID == preference_id).all()

    def create(self, item: PreferencePrice):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: PreferencePrice):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: PreferencePrice):
        self.db.delete(item)
        self.db.commit()
        return True
