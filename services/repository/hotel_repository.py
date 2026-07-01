from sqlalchemy.orm import Session
from models import Hotel


class HotelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Hotel).order_by(Hotel.HotelID).all()

    def get_by_id(self, hotel_id: int):
        return self.db.query(Hotel).filter(Hotel.HotelID == hotel_id).first()

    def get_by_address(self, address: str):
        return self.db.query(Hotel).filter(Hotel.Address.ilike(f"%{address}%")).all()

    def get_kosher(self):
        return self.db.query(Hotel).filter(Hotel.Kosher.is_(True)).all()

    def create(self, hotel: Hotel):
        self.db.add(hotel)
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def update(self, hotel: Hotel):
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def delete(self, hotel: Hotel):
        self.db.delete(hotel)
        self.db.commit()
        return True
