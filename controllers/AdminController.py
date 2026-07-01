import os
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from assignment.assignment_engine import AssignmentEngine
from database.dependencies import get_db
from services.repository.user_repository import UserRepository

router = APIRouter(prefix="/admin", tags=["Admin"])
security = HTTPBearer(auto_error=False)

ACTIVE_TOKENS: dict[str, str] = {}
ACTIVE_ADMIN_PASSWORD: str | None = None


def get_admin_password() -> str | None:
    env_password = os.getenv("ADMIN_PASSWORD", "").strip()
    if env_password:
        return env_password
    return ACTIVE_ADMIN_PASSWORD


class AdminLoginRequest:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


def create_admin_token(username: str) -> str:
    token = uuid.uuid4().hex
    ACTIVE_TOKENS[token] = username
    return token


def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    token = credentials.credentials
    if not token or token not in ACTIVE_TOKENS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return {"username": ACTIVE_TOKENS[token], "db": db}


@router.post("/login")
def admin_login(payload: dict[str, Any]):
    username = payload.get("username")
    password = (payload.get("password") or "").strip()
    configured_password = get_admin_password()

    if username != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")

    if configured_password:
        if password == configured_password:
            token = create_admin_token(username)
            return {
                "access_token": token,
                "token_type": "bearer",
                "message": "Admin authenticated successfully",
            }
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")

    if password:
        global ACTIVE_ADMIN_PASSWORD
        ACTIVE_ADMIN_PASSWORD = password
        token = create_admin_token(username)
        return {
            "access_token": token,
            "token_type": "bearer",
            "message": "Admin password set successfully",
        }

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")


@router.post("/change-password")
def change_admin_password(payload: dict[str, Any], admin=Depends(get_current_admin)):
    global ACTIVE_ADMIN_PASSWORD

    current_password = (payload.get("current_password") or "").strip()
    new_password = (payload.get("new_password") or "").strip()

    if not new_password:
        raise HTTPException(status_code=400, detail="new_password is required")

    configured_password = get_admin_password()
    if configured_password and current_password != configured_password:
        raise HTTPException(status_code=401, detail="Current password is incorrect")

    if not configured_password and current_password:
        if current_password != ACTIVE_ADMIN_PASSWORD:
            raise HTTPException(status_code=401, detail="Current password is incorrect")

    ACTIVE_ADMIN_PASSWORD = new_password
    return {"message": "Admin password updated successfully"}


@router.get("/dashboard")
def admin_dashboard(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    users = UserRepository(db).get_all()
    credit_users = [user for user in users if (user.Credit or 0) > 0]

    return {
        "admin": admin["username"],
        "registered_count": len(users),
        "credit_users_count": len(credit_users),
        "credit_numbers": [float(user.Credit) for user in credit_users],
    }


@router.get("/users")
def admin_users(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    users = UserRepository(db).get_all()
    return [
        {
            "UserID": user.UserID,
            "Name": user.Name,
            "Phone": user.Phone,
            "Email": user.Email,
            "Credit": float(user.Credit) if user.Credit is not None else 0,
        }
        for user in users
    ]


@router.get("/registrations/count")
def admin_registration_count(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    count = UserRepository(db).get_all()
    return {"registered_count": len(count)}


@router.post("/assignments/run")
def admin_run_assignment(payload: dict[str, Any], admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    vacation_id = payload.get("vacation_id")
    hotel_id = payload.get("hotel_id")

    if vacation_id is None:
        raise HTTPException(status_code=400, detail="vacation_id is required")

    try:
        engine = AssignmentEngine(db)
        result = engine.run(vacation_id=vacation_id, hotel_id=hotel_id)
        return {"message": "Assignment algorithm started", "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
