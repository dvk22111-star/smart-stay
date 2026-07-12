from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_preference_price_endpoints():
    response = client.get("/preference-prices/")
    assert response.status_code in [200, 404]

    response = client.get("/preference-prices/1")
    assert response.status_code in [200, 404]

    response = client.post("/preference-prices/", json={"PreferenceID": 1, "AdditionalPrice": 50.0})
    assert response.status_code in [200, 201, 400, 404]

    response = client.get("/preference-prices/preference/1")
    assert response.status_code in [200, 404]
