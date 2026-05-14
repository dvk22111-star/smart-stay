from repositories.placement_repository import PlacementRepository
from models.placement import Placement

class PlacementService:
    def __init__(self, repo: PlacementRepository):
        self.repo = repo

    def create_placement(self, room_id, price, vacationers_customers_id):
        placement = Placement(room_id=room_id, price=price, vacationers_customers_id=vacationers_customers_id)
        return self.repo.add(placement)

    def get_all_placements(self):
        return self.repo.list_all()
