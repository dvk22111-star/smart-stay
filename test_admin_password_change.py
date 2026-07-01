import os

from fastapi.testclient import TestClient

import controllers.AdminController as admin_controller
from main import app

client = TestClient(app)


def test_admin_can_change_password_after_login():
    os.environ.pop('ADMIN_PASSWORD', None)
    admin_controller.ACTIVE_ADMIN_PASSWORD = None
    login_response = client.post('/admin/login', json={'username': 'admin', 'password': 'first-password'})
    assert login_response.status_code == 200
    token = login_response.json().get('access_token')

    change_response = client.post(
        '/admin/change-password',
        json={'current_password': 'first-password', 'new_password': 'second-password'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert change_response.status_code == 200

    second_login = client.post('/admin/login', json={'username': 'admin', 'password': 'second-password'})
    assert second_login.status_code == 200
