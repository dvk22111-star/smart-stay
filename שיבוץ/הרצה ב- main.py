# main.py
from controller.assignment_controller import assign_rooms

if __name__ == "__main__":
    assignments = assign_rooms()
    for room_id, users in assignments.items():
        print(f"Room {room_id}: {users}")