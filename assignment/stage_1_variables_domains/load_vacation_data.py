from sqlalchemy.orm import Session
from models import (
    User,
    Room,
    CustomerPreferences,
    RoomPreferences,
    PartnerRequest,
    Group,
    GroupMembers,
)


def load_vacation_data(session: Session, vacation_id: int, hotel_id: int):
    # משתמשים בנופש
    users = (
        session.query(User)
        .join(CustomerPreferences)
        .filter(CustomerPreferences.VacationID == vacation_id)
        .all()
    )

    # חדרים של המלון בנופש
    rooms = session.query(Room).filter(Room.HotelID == hotel_id).all()

    # העדפות לקוחות (רלוונטיות לנופש)
    customer_prefs = (
        session.query(CustomerPreferences)
        .filter(CustomerPreferences.VacationID == vacation_id)
        .all()
    )

    # העדפות חדרים - סינון לפי חדרים ברשימה
    room_ids = [r.RoomID for r in rooms]
    room_prefs = (
        session.query(RoomPreferences)
        .filter(RoomPreferences.RoomID.in_(room_ids))
        .all()
    )

    # בקשות לשותפים רלוונטיות לנופש
    partner_requests = (
        session.query(PartnerRequest)
        .filter(PartnerRequest.VacationID == vacation_id)
        .all()
    )

    # קבוצות וחברים רלוונטיים לנופש
    groups = session.query(Group).filter(Group.VacationID == vacation_id).all()
    group_ids = [g.GroupID for g in groups]
    group_members = (
        session.query(GroupMembers)
        .filter(GroupMembers.GroupID.in_(group_ids))
        .all()
    )

    return {
        "users": users,
        "rooms": rooms,
        "customer_prefs": customer_prefs,
        "room_prefs": room_prefs,
        "partner_requests": partner_requests,
        "groups": groups,
        "group_members": group_members,
    }
