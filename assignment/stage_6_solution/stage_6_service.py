from .solution_extractor import extract_solution
from .placement_builder import build_placements
from .placement_saver import save_placements
from .excel_exporter import export_to_excel
from .solution_report_builder import build_report

def placement_to_dict(p):
    return {
        "PlacementID": p.PlacementID,
        "RoomID": p.RoomID,
        "VacationersCustomersID": p.VacationersCustomersID,
        "Price": p.Price
    }

def run_stage_6(
    model_vars,
    solver,
    db_session,
    vacation_id,
    price_lookup,
    total_users,
    vacation_customers,
    context
):

    # 1️⃣ חילוץ פתרון

    assignments = extract_solution(
        model_vars,
        solver
    )

    # 2️⃣ יצירת Placements

    placements = build_placements(
        assignments,
        vacation_id,
        price_lookup,
        vacation_customers
    )
    # 3️⃣ שמירה למסד

    save_placements(
        placements,
        db_session
    )

    # 4️⃣ יצוא Excel

    excel_export_result = export_to_excel(
        assignments,
        users=context.users,
        rooms=context.rooms,
        group_members=context.group_members,
        customer_preferences=context.customer_preferences,
        room_preferences=context.room_preferences,
        partner_requests=context.partner_requests,
        filename_prefix=f"vacation_{vacation_id}"
    )

    # 5️⃣ דו"ח

    report = build_report(
        assignments,
        total_users
    )

    return {
        "assignments": assignments,
        "placements": [placement_to_dict(p) for p in placements],
        "report": report,
        "excel_export": excel_export_result,
    }