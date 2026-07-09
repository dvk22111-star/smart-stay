import os
import pandas as pd
from .excel_report_builder import build_report_tables

EXCELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "excels")


def ensure_excels_dir():
    os.makedirs(EXCELS_DIR, exist_ok=True)


def _save_table(df, filename):
    ensure_excels_dir()
    path = os.path.abspath(os.path.join(EXCELS_DIR, filename))
    df.to_excel(path, index=False)
    return path


def export_to_excel(
    assignments,
    users,
    rooms,
    group_members,
    customer_preferences,
    room_preferences,
    filename_prefix="solution"
):
    """
    יצירת קבצי Excel של השיבוץ והדוחות הנלווים.
    """
    report_tables = build_report_tables(
        assignments,
        users,
        rooms,
        group_members,
        customer_preferences,
        room_preferences,
    )

    result = {}

    if report_tables["assignments"]:
        df_assignments = pd.DataFrame(report_tables["assignments"])
        result["assignments"] = _save_table(
            df_assignments,
            f"{filename_prefix}_assignments.xlsx"
        )

    if report_tables["empty_rooms"]:
        df_empty = pd.DataFrame(report_tables["empty_rooms"])
        result["empty_rooms"] = _save_table(
            df_empty,
            f"{filename_prefix}_empty_rooms.xlsx"
        )

    if report_tables["free_beds"]:
        df_free = pd.DataFrame(report_tables["free_beds"])
        result["free_beds"] = _save_table(
            df_free,
            f"{filename_prefix}_free_beds.xlsx"
        )

    if report_tables["missing_women"]:
        df_missing = pd.DataFrame(report_tables["missing_women"])
        result["missing_women"] = _save_table(
            df_missing,
            f"{filename_prefix}_missing_women.xlsx"
        )

    if report_tables["low_score_women"]:
        df_low_score = pd.DataFrame(report_tables["low_score_women"])
        result["low_score_women"] = _save_table(
            df_low_score,
            f"{filename_prefix}_low_score_women.xlsx"
        )

    return {
        "paths": result,
        "tables": report_tables,
    }
