from services.repository.placement_repository import PlacementRepository


def save_placements(placements, db_session):
    """שמור רשימת `Placement` למסד באמצעות `PlacementRepository.create`."""
    repo = PlacementRepository(db_session)
    for placement in placements:
        repo.create(placement)