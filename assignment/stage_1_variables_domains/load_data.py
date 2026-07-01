from sqlalchemy.orm import Session
from models import User, Room, CustomerPreferences, RoomPreferences, PartnerRequest, Group, GroupMembers


def load_vacation_data(session: Session, vacation_id: int):
    # משתמשים בנופש
    users = session.query(User).join(CustomerPreferences).filter(CustomerPreferences.VacationID == vacation_id).all()

    # חדרים בנופש
    rooms = session.query(Room).join(RoomPreferences).filter(Room.HotelID == vacation_id).all()

    # העדפות לקוחות
    customer_prefs = session.query(CustomerPreferences).filter(CustomerPreferences.VacationID == vacation_id).all()

    # העדפות חדרים
    room_prefs = session.query(RoomPreferences).all()

    # בקשות לשותפים
    partner_requests = session.query(PartnerRequest).filter(PartnerRequest.VacationID == vacation_id).all()

    # קבוצות וחברים
    groups = session.query(Group).filter(Group.VacationID == vacation_id).all()
    group_members = session.query(GroupMembers).all()

    return {
        "users": users,
        "rooms": rooms,
        "customer_prefs": customer_prefs,
        "room_prefs": room_prefs,
        "partner_requests": partner_requests,
        "groups": groups,
        "group_members": group_members
    }