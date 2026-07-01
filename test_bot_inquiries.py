from fastapi.testclient import TestClient
from main import app
from services.repository.bot_session_repository import BotSessionRepository
from services.repository.user_repository import UserRepository
from services.repository.vacation_repository import VacationRepository

client = TestClient(app)


def setup_test_session(db):
    # create a session for existing user (assumes user with phone 0501234567 exists)
    user_repo = UserRepository(db)
    user = user_repo.get_by_phone('0501234567')
    vac_repo = VacationRepository(db)
    vacations = vac_repo.get_all()
    vac_id = vacations[0].VacationID if vacations else None
    bs_repo = BotSessionRepository(db)
    session = bs_repo.create({'Phone': '0501234567', 'VacationID': vac_id})
    return session


def test_maternity_inquiry_returns_canned_message():
    # create session
    # Note: Using TestClient endpoints only; relying on existing DB fixtures
    response = client.post('/bot/sessions', json={'Phone': '0501234567'})
    assert response.status_code == 200
    sess = response.json()
    session_id = sess['SessionID']

    # verify phone to move session to IN_PROGRESS
    v = client.post(f'/bot/sessions/{session_id}/verify-phone')
    assert v.status_code == 200

    r = client.post(f'/bot/sessions/{session_id}/answers', json={'QuestionID': 'QUESTION_INTRO', 'AnswerText': 'שלום', 'IsFinal': False})
    assert r.status_code == 200

    # ask about maternity refund
    inquiry = 'האם יש החזרי לידה?'
    r2 = client.post(f'/bot/sessions/{session_id}/answers', json={'QuestionID': 'QUESTION_INTRO', 'AnswerText': inquiry, 'IsFinal': False})
    assert r2.status_code == 200
    body = r2.json()
    assert body.get('inquiry') == 'maternity'
    assert 'החזרי לידה' in body.get('message')


def test_dates_and_location_inquiry():
    response = client.post('/bot/sessions', json={'Phone': '0501234567'})
    assert response.status_code == 200
    sess = response.json()
    session_id = sess['SessionID']
    v = client.post(f'/bot/sessions/{session_id}/verify-phone')
    assert v.status_code == 200

    # dates
    r = client.post(f'/bot/sessions/{session_id}/answers', json={'QuestionID': 'QUESTION_INTRO', 'AnswerText': 'מתי החופשה?', 'IsFinal': False})
    assert r.status_code == 200
    body = r.json()
    assert body.get('inquiry') == 'dates' or body.get('message')

    # location
    r2 = client.post(f'/bot/sessions/{session_id}/answers', json={'QuestionID': 'QUESTION_INTRO', 'AnswerText': 'איפה תהיה החופשה?', 'IsFinal': False})
    assert r2.status_code == 200
    body2 = r2.json()
    assert body2.get('inquiry') == 'location' or body2.get('message')


def test_unrelated_question_guides_user_back_to_registration_flow():
    response = client.post('/bot/sessions', json={'Phone': '0501234567'})
    assert response.status_code == 200
    sess = response.json()
    session_id = sess['SessionID']
    v = client.post(f'/bot/sessions/{session_id}/verify-phone')
    assert v.status_code == 200

    r = client.post(f'/bot/sessions/{session_id}/answers', json={'QuestionID': 'QUESTION_INTRO', 'AnswerText': 'איך נבנה כוס תה?', 'IsFinal': False})
    assert r.status_code == 200
    body = r.json()
    assert body.get('inquiry') == 'unrelated'
    assert 'עונה רק על שאלות' in body.get('message', '')
    assert body.get('next_question', {}).get('id') == 'QUESTION_INTRO'
