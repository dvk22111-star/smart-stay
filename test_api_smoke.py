from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def assert_ok(response, expected_status=(200,)):
    assert response.status_code in expected_status, (
        f"Expected {expected_status}, got {response.status_code}: {response.text}"
    )


def test_root_endpoint():
    response = client.get("/")
    assert_ok(response)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert_ok(response)


def test_users_endpoints():
    assert_ok(client.get("/users/"))
    assert_ok(client.get("/users/1"), expected_status=(200, 404))
    assert_ok(client.get("/users/phone/0500000000"), expected_status=(200, 404))
    assert_ok(client.get("/users/search?name=a"))
    assert_ok(client.get("/users/credit/high"))


def test_hotels_endpoints():
    assert_ok(client.get("/hotels/"))
    assert_ok(client.get("/hotels/1"), expected_status=(200, 404))
    assert_ok(client.get("/hotels/city?address=a"))
    assert_ok(client.get("/hotels/kosher"))
    assert_ok(client.get("/hotels/available-rooms"))


def test_rooms_endpoints():
    assert_ok(client.get("/rooms/"))
    assert_ok(client.get("/rooms/1"), expected_status=(200, 404))
    assert_ok(client.get("/rooms/hotel/1"), expected_status=(200, 404))
    assert_ok(client.get("/rooms/beds/1"))
    assert_ok(client.get("/rooms/floor/1"))


def test_vacations_endpoints():
    assert_ok(client.get("/vacations/"))
    assert_ok(client.get("/vacations/1"), expected_status=(200, 404))
    assert_ok(client.get("/vacations/active"))
    assert_ok(client.get("/vacations/future"))
    assert_ok(client.get("/vacations/hotel/1"), expected_status=(200, 404))


def test_groups_endpoints():
    assert_ok(client.get("/groups/"))
    assert_ok(client.get("/groups/1"), expected_status=(200, 404))
    assert_ok(client.get("/groups/vacation/1"), expected_status=(200, 404))
    assert_ok(client.get("/groups/size/1"))


def test_group_members_endpoints():
    assert_ok(client.get("/group-members/"))
    assert_ok(client.get("/group-members/group/1"), expected_status=(200, 404))


def test_workers_endpoints():
    assert_ok(client.get("/workers/"))
    assert_ok(client.get("/workers/email/test@example.com"), expected_status=(200, 404))
    assert_ok(client.get("/workers/active"))


def test_permissions_endpoints():
    assert_ok(client.get("/permissions/"))
    assert_ok(client.get("/permissions/type/ADMIN"), expected_status=(200, 404))


def test_preferences_endpoints():
    assert_ok(client.get("/preferences/"))
    assert_ok(client.get("/preferences/1"), expected_status=(200, 404))
    assert_ok(client.get("/preferences/search/a"))
    assert_ok(client.get("/preferences/type/SEA_VIEW"), expected_status=(200, 404))


def test_placements_endpoints():
    assert_ok(client.get("/placements/room/1"), expected_status=(200, 404))
    assert_ok(client.get("/placements/vacation/1"), expected_status=(200, 404))
    assert_ok(client.get("/placements/available"))


def test_customer_preferences_endpoints():
    assert_ok(client.get("/customer-preferences/"))
    assert_ok(client.get("/customer-preferences/user/1"), expected_status=(200, 404))


def test_hotel_preferences_endpoints():
    assert_ok(client.get("/hotel-preferences/"))
    assert_ok(client.get("/hotel-preferences/hotel/1"), expected_status=(200, 404))


def test_room_preferences_endpoints():
    assert_ok(client.get("/room-preferences/"))
    assert_ok(client.get("/room-preferences/room/1"), expected_status=(200, 404))


def test_partner_requests_endpoints():
    assert_ok(client.get("/partner-requests/"))
    assert_ok(client.get("/partner-requests/user/1"), expected_status=(200, 404))


def test_vacationers_customers_endpoints():
    assert_ok(client.get("/vacationers-customers/"))
    assert_ok(client.get("/vacationers-customers/unassigned"))
    assert_ok(client.get("/vacationers-customers/assigned"))
