from repositories.vacation_repository import VacationRepository
from models.vacation import Vacation

class VacationService:
    def __init__(self, repo: VacationRepository):
        self.repo = repo

    def create_vacation(self, hotel_id, start, end, program_link, basic_cost, number_of_rooms, number_of_floors):
        vacation = Vacation(
            hotel_id=hotel_id,
            start=start,
            end=end,
            program_link=program_link,
            basic_cost=basic_cost,
            number_of_rooms=number_of_rooms,
            number_of_floors=number_of_floors
        )
        return self.repo.add(vacation)

    def get_all_vacations(self):
        return self.repo.list_all()
