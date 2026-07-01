from .solution_extractor import extract_solution
from .placement_builder import build_placements
from .placement_saver import save_placements
from .excel_exporter import export_to_excel
from .solution_report_builder import build_report


def run_stage_6(
    model_vars,
    solver,
    db_session,
    vacation_id,
    price_lookup,
    total_users,
    vacation_customers
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

    export_to_excel(
        assignments,
        db_session
    )

    # 5️⃣ דו"ח

    report = build_report(
        assignments,
        total_users
    )

    return {
        "assignments": assignments,
        "placements": placements,
        "report": report
    }