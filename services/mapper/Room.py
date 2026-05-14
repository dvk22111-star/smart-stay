
from repositories.room_repository import RoomRepository
from models.room import Room

class RoomService:
    def __init__(self, repo: RoomRepository):
        self.repo = repo

    def create_room(self, room_number, floor, hotel_id, number_of_beds):
        room = Room(room_number=room_number, floor=floor, hotel_id=hotel_id, number_of_beds=number_of_beds)
        return self.repo.add(room)

    def get_all_rooms(self):
        return self.repo.list_all()
