

from repositories.hotel_repository import HotelRepository
from models.hotel import Hotel

class HotelService:
    def __init__(self, repo: HotelRepository):
        self.repo = repo

    def create_hotel(self, name, address, kosher=True, contact_person=""):
        hotel = Hotel(name=name, address=address, kosher=kosher, contact_person=contact_person)
        return self.repo.add(hotel)

    def get_all_hotels(self):
        return self.repo.list_all()
