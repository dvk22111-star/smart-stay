from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
app = FastAPI(
    title="Smart Stay API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
         "http://127.0.0.1:5175",
           "http://127.0.0.1:5176",

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# IMPORT ROUTERS
# ==========================

from controllers.UserController import router as users_router
from controllers.HotelController import router as hotels_router
from controllers.RoomController import router as rooms_router
from controllers.VacationController import router as vacations_router
from controllers.AssignmentController import router as assignments_router
from controllers.GroupController import router as groups_router
from controllers.GroupMembersController import router as group_members_router
from controllers.WorkerController import router as workers_router
from controllers.PermissionsController import router as permissions_router
from controllers.PreferencesController import router as preferences_router
from controllers.VacationersCustomersController import router as vacationers_router
from controllers.PlacementController import router as placements_router
from controllers.CustomerPreferencesController import router as customer_preferences_router
from controllers.HotelPreferencesController import router as hotel_preferences_router
from controllers.RoomPreferencesController import router as room_preferences_router
from controllers.PreferencePriceController import router as preference_price_router
from controllers.PriceController import router as price_router
from controllers.PartnerRequestsController import router as partner_requests_router
from controllers.BotController import router as bot_router
from controllers.AdminController import router as admin_router

from fastapi import HTTPException

@app.post("/chat/message")
def chat_message(payload: dict):
    message = (payload.get("message") or "").strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    from bot.flow import get_question, next_question
    from controllers.BotController import SESSIONS, InMemoryStatus
    from datetime import datetime

    session_id = payload.get("session_id")
    if session_id is None:
        session_id = 1

    session = SESSIONS.get(session_id)
    if not session:
        session = {
            "SessionID": session_id,
            "UserID": None,
            "VacationID": payload.get("vacation_id"),
            "GroupID": payload.get("group_id"),
            "Phone": payload.get("phone") or "",
            "Status": InMemoryStatus.AWAITING_VERIFICATION,
            "CurrentQuestionID": None,
            "CreatedAt": datetime.utcnow(),
            "UpdatedAt": datetime.utcnow(),
        }
        SESSIONS[session_id] = session

    if session.get("Status") != InMemoryStatus.IN_PROGRESS:
        session["Status"] = InMemoryStatus.IN_PROGRESS
        session["CurrentQuestionID"] = session.get("CurrentQuestionID") or "QUESTION_NAME"

    from bot.flow import handle_answer
    from bot.parser import detect_inquiry

    question_id = session.get("CurrentQuestionID") or "QUESTION_INTRO"
    inquiry = detect_inquiry(message)
    if inquiry == "maternity":
        return {
            "reply": "יש לנו החזרי לידה אך הדבר צריך להיות מסודר מול המלון ולא דרכנו.",
            "session_id": session_id,
            "next_question": get_question(question_id),
        }

    if inquiry == "unrelated":
        return {
            "reply": "אני עונה רק על שאלות הקשורות לנופש והרשמה.",
            "session_id": session_id,
            "next_question": get_question(question_id),
        }

    parse_result = handle_answer(question_id, message)
    next_q = parse_result.get("next_question") or next_question(question_id)
    if isinstance(next_q, dict):
        next_question_id = next_q["id"]
    else:
        next_question_id = next_q

    session["CurrentQuestionID"] = next_question_id
    session["UpdatedAt"] = datetime.utcnow()
    return {
        "reply": get_question(next_question_id).get("text") if get_question(next_question_id) else "תודה!",
        "session_id": session_id,
        "next_question": get_question(next_question_id),
    }

# ==========================
# REGISTER ROUTERS
# ==========================

app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(vacations_router)
app.include_router(groups_router)
app.include_router(group_members_router)
app.include_router(workers_router)
app.include_router(permissions_router)
app.include_router(preferences_router)
app.include_router(vacationers_router)
app.include_router(placements_router)
app.include_router(assignments_router)
app.include_router(customer_preferences_router)
app.include_router(hotel_preferences_router)
app.include_router(room_preferences_router)
app.include_router(preference_price_router)
app.include_router(price_router)
app.include_router(partner_requests_router)
app.include_router(bot_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Smart Stay API Running"}