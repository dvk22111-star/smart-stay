from loaders.user_loader import load_users
from loaders.room_loader import load_rooms
from loaders.partner_request_loader import load_partner_requests
from loaders.customer_preferences_loader import load_customer_preferences
from assignment.assigner import assign_rooms

users = load_users("data/users.json")
rooms = load_rooms("data/rooms.json")
partner_requests = load_partner_requests("data/partner_requests.json")
customer_preferences = load_customer_preferences("data/customer_preferences.json")

assignments = assign_rooms(users, rooms, partner_requests, customer_preferences)

for room_id, occupants in assignments.items():
    print(f"Room {room_id}: {occupants}")