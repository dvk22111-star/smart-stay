import os

from fastapi.testclient import TestClient

import controllers.AdminController as admin_controller
from main import app

client = TestClient(app)


def reset_admin_state():
    os.environ.pop('ADMIN_PASSWORD', None)
    admin_controller.ACTIVE_ADMIN_PASSWORD = None


def test_admin_login_and_dashboard_access():
    reset_admin_state()
    chosen_password = 'my-admin-password'
    login_response = client.post('/admin/login', json={'username': 'admin', 'password': chosen_password})
    assert login_response.status_code == 200
    token = login_response.json().get('access_token')
    assert token

    dashboard_response = client.get('/admin/dashboard', headers={'Authorization': f'Bearer {token}'})
    assert dashboard_response.status_code == 200
    body = dashboard_response.json()
    assert 'registered_count' in body
    assert 'credit_users_count' in body


def test_admin_endpoints_require_auth():
    reset_admin_state()
    response = client.get('/admin/users')
    assert response.status_code == 401
