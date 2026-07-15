from sqlalchemy import text
from database.connection import SessionLocal
from models import Group, GroupMembers, User
import sys


def normalize_phone(phone):
    return (phone or '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '').strip()


def run_checks(vacation_id=1):
    s = SessionLocal()
    groups = s.query(Group).filter(Group.VacationID == vacation_id).all()
    if not groups:
        print(f"No groups found for vacation_id={vacation_id}")
        return 0

    group_ids = [g.GroupID for g in groups]
    members = s.query(GroupMembers).filter(GroupMembers.GroupID.in_(group_ids)).all()

    users = s.query(User).all()
    users_map = {u.UserID: u for u in users}
    users_by_phone = {normalize_phone(u.Phone): u for u in users if getattr(u, 'Phone', None)}

    issues = []

    print(f"Found {len(groups)} groups, {len(members)} group_members, {len(users)} users")

    members_by_group = {}
    for m in members:
        members_by_group.setdefault(m.GroupID, []).append(m)

    for g in groups:
        mids = members_by_group.get(g.GroupID, [])
        print(f"\nGroup {g.GroupID}: NumberofParticipants={g.NumberofParticipants}, members_records={len(mids)}")

        # 1. existence: all group_members map to a user by phone
        unresolved = []
        seen_user_ids = set()
        for m in mids:
            phone = normalize_phone(m.Telephone)
            u = users_by_phone.get(phone)
            if not u:
                unresolved.append(m)
            else:
                seen_user_ids.add(u.UserID)

        if unresolved:
            issues.append((g.GroupID, 'unresolved_members', [m.IDOfGroupMembers for m in unresolved]))
            print(f"  Unresolved members (no matching user by phone): {[m.IDOfGroupMembers for m in unresolved]}")
        else:
            print(f"  All group_members resolved to users: {sorted(list(seen_user_ids))}")

        # 1b. Group.UserID must exist in users if set
        if getattr(g, 'UserID', None) and g.UserID not in users_map:
            issues.append((g.GroupID, 'group_admin_missing', g.UserID))
            print(f"  WARNING: group.UserID {g.UserID} not found in users table")

        # 2. NumberofParticipants vs count(group_members)
        count_members = len(mids)
        if g.NumberofParticipants is not None and g.NumberofParticipants != count_members:
            issues.append((g.GroupID, 'size_mismatch', {'NumberofParticipants': g.NumberofParticipants, 'group_members_count': count_members}))
            print(f"  SIZE MISMATCH: NumberofParticipants={g.NumberofParticipants} vs group_members_count={count_members}")
        else:
            print(f"  Size match or missing NumberofParticipants: {g.NumberofParticipants} == {count_members}")

        # 3. duplicates
        phones = [normalize_phone(m.Telephone) for m in mids]
        dup_phones = set([p for p in phones if phones.count(p) > 1 and p])
        if dup_phones:
            issues.append((g.GroupID, 'duplicate_members_by_phone', list(dup_phones)))
            print(f"  DUPLICATES by phone: {list(dup_phones)}")
        else:
            print("  No duplicate phones among members")

        # 4. members without vacation: GroupMembers has no vacation field — check users' vacations via VacationersCustomers
        # We'll attempt to verify that resolved users are registered for this vacation
        from models import VacationersCustomers
        bad_vac = []
        for m in mids:
            phone = normalize_phone(m.Telephone)
            u = users_by_phone.get(phone)
            if not u:
                continue
            rows = s.query(VacationersCustomers).filter_by(UserID=u.UserID, VacationID=vacation_id).count()
            if rows == 0:
                bad_vac.append(u.UserID)
        if bad_vac:
            issues.append((g.GroupID, 'member_not_registered_for_vacation', bad_vac))
            print(f"  Members not registered for vacation {vacation_id}: {bad_vac}")
        else:
            print("  All resolved members are registered for vacation")

    print('\nSummary:')
    if not issues:
        print('  No issues found')
    else:
        for it in issues:
            print(' ', it)

    return len(issues)


if __name__ == '__main__':
    vid = 1
    if len(sys.argv) > 1:
        try:
            vid = int(sys.argv[1])
        except Exception:
            pass
    rc = run_checks(vid)
    sys.exit(0 if rc == 0 else 2)
