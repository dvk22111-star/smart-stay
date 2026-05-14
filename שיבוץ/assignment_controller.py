# controller/assignment_controller.py   - קריאה לאלגוריתם.
from service.assignment_service import full_optimal_assignment
from model.user import User
from model.room import Room
from model.group import Group
from model.customer_preference import CustomerPreference
from model.partner_request import PartnerRequest

def assign_rooms():
    users = User.get_all()
    rooms = Room.get_all()
    partner_requests = PartnerRequest.get_all()
    customer_preferences = CustomerPreference.get_all()
    groups = Group.get_all()
    all_group_members = Group.get_all_members()

    return full_optimal_assignment(
        users, rooms, partner_requests, customer_preferences, groups, all_group_members
    )