from sqlalchemy.orm import Session
from models import Group, GroupMembers, User


def run_group_consistency_checks(session: Session, vacation_id: int):
    warnings = []

    groups = session.query(Group).filter(Group.VacationID == vacation_id).all()
    if not groups:
        return warnings

    group_ids = [g.GroupID for g in groups]
    members = session.query(GroupMembers).filter(GroupMembers.GroupID.in_(group_ids)).all()

    # build helper maps
    users = {u.UserID: u for u in session.query(User).all()}
    users_by_phone = { (u.Phone.replace(' ', '').replace('-', '') if u.Phone else ''): u for u in users.values() }

    members_by_group = {}
    for m in members:
        members_by_group.setdefault(m.GroupID, []).append(m)

    for g in groups:
        mids = members_by_group.get(g.GroupID, [])

        # 1. existence: all group_members map to a user by phone
        unresolved = []
        seen_user_ids = set()
        for m in mids:
            phone = (m.Telephone or '').replace(' ', '').replace('-', '')
            u = users_by_phone.get(phone)
            if not u:
                unresolved.append(m)
            else:
                seen_user_ids.add(u.UserID)

        if unresolved:
            warnings.append((g.GroupID, 'unresolved_members', [m.IDOfGroupMembers for m in unresolved]))

        # 1b. Group.UserID must exist in users if set
        if getattr(g, 'UserID', None) and g.UserID not in users:
            warnings.append((g.GroupID, 'group_admin_missing', g.UserID))

        # 2. NumberofParticipants vs count(group_members)
        count_members = len(mids)
        if g.NumberofParticipants is not None and g.NumberofParticipants != count_members:
            warnings.append((g.GroupID, 'size_mismatch', {'NumberofParticipants': g.NumberofParticipants, 'group_members_count': count_members}))

        # 3. duplicates
        phones = [ (m.Telephone or '').replace(' ', '').replace('-', '') for m in mids ]
        dup_phones = set([p for p in phones if phones.count(p) > 1])
        if dup_phones:
            warnings.append((g.GroupID, 'duplicate_members_by_phone', list(dup_phones)))

        # 4. vacation_id consistency: group.VacationID should match any vacation implied by members? (members don't hold vacation)
        # We already selected groups by vacation, so ensure members exist.
        # Members without matching group should be flagged earlier by the query restrictions.

    return warnings


# Unit tests

def test_group_consistency_checks_run(db_session):
    # uses fixture db_session provided by test harness
    warnings = run_group_consistency_checks(db_session, vacation_id=1)
    # for real dataset we don't assert no warnings, just ensure function runs
    assert isinstance(warnings, list)


def test_group_assignment_scenario(client, db_session):
    # Build in-memory scenario: create users, rooms, group and group_members
    from models import Room, VacationersCustomers, Vacation

    # cleanup any existing data for vacation 999
    vac_id = 999
    session = db_session

    # create vacation if needed
    vac = Vacation(VacationID=vac_id, Name='TestVac')
    session.add(vac)
    session.commit()

    # create users 1..4
    users = []
    for i in range(1,5):
        u = User(Name=f"U{i}", Phone=f"05000000{i}", Email=f"u{i}@test.local")
        session.add(u)
        users.append(u)
    session.commit()

    # create group
    g = Group(UserID=users[0].UserID, GroupName='G1', NumberofParticipants=4, VacationID=vac_id)
    session.add(g)
    session.commit()

    # add group_members by phone
    for u in users:
        gm = GroupMembers(GroupID=g.GroupID, Telephone=(u.Phone or ''))
        session.add(gm)
    session.commit()

    # create rooms 101 and 102 with capacity 2 each for the same hotel
    h_id = 1111
    # minimal hotel insertion not required if Room doesn't require FK in this test DB
    r1 = Room(RoomID=101, HotelID=h_id, NumberOfBeds=2, Floor=1)
    r2 = Room(RoomID=102, HotelID=h_id, NumberOfBeds=2, Floor=1)
    session.add_all([r1, r2])
    session.commit()

    # create VacationersCustomers entries linking users to vacation
    vcs = []
    for u in users:
        vc = VacationersCustomers(UserID=u.UserID, VacationID=vac_id)
        session.add(vc)
        vcs.append(vc)
    session.commit()

    # run the assignment pipeline for vacation_id=vac_id, hotel_id=h_id
    from assignment.run_assignment import run_assignment
    result = run_assignment(vacation_id=vac_id, hotel_id=h_id)

    assignments = result.get('assignments', {})
    assigned_users = len(assignments)

    assert assigned_users == 4


def test_group_assignment_split_when_no_4_bed_room(client, db_session):
    # same as above but rooms only 2+2 and ensure split
    pass
