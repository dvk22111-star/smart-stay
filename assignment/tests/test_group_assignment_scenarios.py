import pytest
from assignment.run_assignment import run
from database.connection import engine
from sqlalchemy.orm import Session
from models import User, Group, GroupMembers, Room, Vacation, VacationersCustomers


@pytest.fixture
def clean_db():
    # create an isolated transactional session using SAVEPOINT (nested transaction)
    conn = engine.connect()
    trans = conn.begin()
    sess = Session(bind=conn)
    sess.begin_nested()
    try:
        yield sess
    finally:
        try:
            sess.rollback()
        finally:
            sess.close()
            trans.rollback()
            conn.close()


def setup_group_and_users(session, vac_id, user_count=4, base_phone='050000001'):
    users = []
    for i in range(user_count):
        u = User(Name=f"U{i+1}", Phone=f"{base_phone}{i}", Email=f"u{i+1}@test.local")
        session.add(u)
        users.append(u)
    session.commit()

    g = Group(UserID=users[0].UserID, GroupName='Gtest', NumberofParticipants=user_count, VacationID=vac_id)
    session.add(g)
    session.commit()

    for u in users:
        gm = GroupMembers(GroupID=g.GroupID, Telephone=(u.Phone or ''))
        session.add(gm)
        from datetime import date
        vc = VacationersCustomers(UserID=u.UserID, VacationID=vac_id, UpdateDate=date.today())
        session.add(vc)
    session.commit()

    return users, g


def run_assignment_for(vac_id, hotel_id):
    # use assignment.run_assignment to run pipeline
    from assignment.run_assignment import run as runner
    # runner prints results; capture via calling
    runner()


def test_group_fits_in_one_room(clean_db):
    s = clean_db
    # Vacation model requires StartV, EndV, BasicCost - provide minimal valid values
    from datetime import date
    vac = Vacation(VacationID=2000, HotelID=1, StartV=date(2026,1,1), EndV=date(2026,1,2), BasicCost=0.0)
    s.add(vac)
    s.commit()

    users, g = setup_group_and_users(s, vac_id=2000, user_count=4, base_phone='0501000')

    # create one room with capacity 4
    # ensure hotel exists for FK
    from models import Hotel
    h = Hotel(HotelID=5000, Name='H5000', Address='Addr')
    s.add(h)
    s.commit()

    r = Room(RoomID=301, RoomNumber='301', HotelID=5000, NumberOfBeds=4, Floor=1)
    s.add(r)
    s.commit()

    # run assignment
    from assignment.assignment_engine import AssignmentEngine
    engine = AssignmentEngine(s)
    res = engine.run(vacation_id=2000, hotel_id=5000)
    assignments = res.get('assignments', {})

    assert len(assignments) == 4
    # all assigned to room 301
    assert all(rid == 301 for rid in assignments.values())


def test_group_splits_across_adjacent_rooms(clean_db):
    s = clean_db
    from datetime import date
    vac = Vacation(VacationID=2001, HotelID=1, StartV=date(2026,1,1), EndV=date(2026,1,2), BasicCost=0.0)
    s.add(vac)
    s.commit()

    users, g = setup_group_and_users(s, vac_id=2001, user_count=4, base_phone='0502000')

    # create two adjacent rooms capacity 2 each
    # ensure hotel exists for FK
    from models import Hotel
    h2 = Hotel(HotelID=6000, Name='H6000', Address='Addr')
    s.add(h2)
    s.commit()

    r1 = Room(RoomID=101, RoomNumber='101', HotelID=6000, NumberOfBeds=2, Floor=1)
    r2 = Room(RoomID=102, RoomNumber='102', HotelID=6000, NumberOfBeds=2, Floor=1)
    s.add_all([r1, r2])
    s.commit()

    from assignment.assignment_engine import AssignmentEngine
    engine = AssignmentEngine(s)
    res = engine.run(vacation_id=2001, hotel_id=6000)
    assignments = res.get('assignments', {})

    assert len(assignments) == 4
    # count per room
    counts = {}
    for uid, rid in assignments.items():
        counts[rid] = counts.get(rid, 0) + 1

    assert counts.get(101, 0) == 2
    assert counts.get(102, 0) == 2
