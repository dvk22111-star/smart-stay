from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ================= USERS =================

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200


def test_get_user_by_phone():
    response = client.get("/users/by_phone/0500000000")
    assert response.status_code in [200, 404]


# ================= HOTELS =================

def test_get_hotels():
    response = client.get("/hotels/")
    assert response.status_code == 200


# ================= ROOMS =================

def test_get_rooms():
    response = client.get("/rooms/")
    assert response.status_code == 200


# ================= VACATIONS =================

def test_get_vacations():
    response = client.get("/vacations/")
    assert response.status_code == 200


# ================= GROUPS =================

def test_get_groups():
    response = client.get("/groups/")
    assert response.status_code == 200


# ================= GROUP MEMBERS =================

def test_get_group_members():
    response = client.get("/group-members/group/1")
    assert response.status_code in [200, 404]


# ================= WORKERS =================

def test_get_workers():
    response = client.get("/workers/")
    assert response.status_code == 200


# ================= PERMISSIONS =================

def test_get_permissions():
    response = client.get("/permissions/")
    assert response.status_code == 200


# ================= VACATIONERS CUSTOMERS =================

def test_get_vacationers():
    response = client.get("/vacationers-customers/unassigned")
    assert response.status_code == 200


# ================= PREFERENCES =================

def test_get_preferences():
    response = client.get("/preferences/")
    assert response.status_code == 200