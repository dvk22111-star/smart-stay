from fastapi import FastAPI

app = FastAPI(
    title="Smart Stay API",
    version="1.0.0"
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
from controllers.PartnerRequestsController import router as partner_requests_router
from controllers.BotController import router as bot_router
from controllers.AdminController import router as admin_router

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
app.include_router(partner_requests_router)
app.include_router(bot_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Smart Stay API Running"}