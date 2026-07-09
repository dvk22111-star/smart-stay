from services.repository.placement_repository import PlacementRepository

def save_placements(placements, db_session):
    print("Count:", len(placements))

    repo = PlacementRepository(db_session)

    for placement in placements:
        print(
            "Saving:",
            placement.RoomID,
            placement.VacationersCustomersID,
            placement.Price,
        )
        repo.create(placement)