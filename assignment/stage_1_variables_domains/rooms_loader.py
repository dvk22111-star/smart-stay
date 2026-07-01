# אחראי על שליפת כל החדרים של המלון בנופש

class RoomsLoader:

    def __init__(self, room_repository):
        self._room_repository = room_repository

    # מחזיר את כל החדרים הזמינים לנופש
    def load(self, hotel_id):

        return self._room_repository.get_by_hotel_id(
            hotel_id
        )