import re
from typing import Optional

YES_VALUES = {"כן", "כן!", "כן.", "yes", "y", "true", "ט"}
NO_VALUES = {"לא", "לא!", "לא.", "no", "n", "false", "פ"}

PREFERENCE_NAME_MAP = {
    "נוף לים": "SEA_VIEW",
    "sea view": "SEA_VIEW",
    "sea-view": "SEA_VIEW",
    "קומה נמוכה": "LOW_FLOOR",
    "קומה נמוך": "LOW_FLOOR",
    "קומה גבוהה": "HIGH_FLOOR",
    "קומה גבוה": "HIGH_FLOOR",
    "קומה עליונה": "HIGH_FLOOR",
    "קומה תחתונה": "LOW_FLOOR",
}

PREFERENCE_PATTERN = re.compile(
    r"(?P<name>נוף לים|sea view|sea-view|קומה נמוכה|קומה נמוך|קומה גבוהה|קומה גבוה|קומה עליונה|קומה תחתונה)\s*(?P<rating>\d+)",
    re.IGNORECASE,
)


def parse_yes_no(answer_text: str) -> Optional[bool]:
    if not answer_text:
        return None

    normalized = answer_text.strip().lower()
    if normalized in YES_VALUES:
        return True
    if normalized in NO_VALUES:
        return False

    # Allow phrasing like 'כן תודה' או 'לא תודה'
    for token in YES_VALUES:
        if token in normalized:
            return True
    for token in NO_VALUES:
        if token in normalized:
            return False

    return None


def detect_inquiry(answer_text: str) -> Optional[str]:
    if not answer_text:
        return None

    normalized = answer_text.strip().lower()

    maternity_keywords = ["לידה", "החזר לידה", "החזרי לידה"]
    if any(keyword in normalized for keyword in maternity_keywords):
        return "maternity"

    date_keywords = ["מתי", "תאריך", "תאריכים", "עד מתי", "תחילת", "סיום", "יום ההגעה", "יום העזיבה", "החופשה מתחילה", "החופשה נגמרת"]
    location_keywords = ["איפה", "כתובת", "מלון", "מיקום", "היכן", "חדר", "במלון"]
    vacation_related_keywords = ["נופש", "חופשה", "מלון", "חדר", "רישום", "העדפה", "העדפות", "הזמנה", "תאריך", "מיקום", "נגיש", "מונגש", "החזר"]

    if any(keyword in normalized for keyword in date_keywords):
        return "dates"

    if any(keyword in normalized for keyword in location_keywords):
        return "location"

    if "?" in answer_text and not any(keyword in normalized for keyword in vacation_related_keywords):
        if any(keyword in normalized for keyword in ["איך", "מה", "למה", "מי", "למי"]) or (
            "האם" in normalized and not any(keyword in normalized for keyword in ["חדר", "מלון", "נופש", "חופשה", "העדפה", "רישום", "הזמנה"])
        ):
            return "unrelated"

    return None


def parse_partner_request(answer_text: str) -> Optional[str]:
    if not answer_text:
        return None

    cleaned = answer_text.strip()
    normalized = cleaned.lower()
    if normalized in {"לא", "אין", "none", "no"}:
        return None

    digits = re.sub(r"\D+", "", cleaned)
    if len(digits) >= 7:
        return digits

    # Fallback: if the answer looks like a phone string with separators
    if any(ch.isdigit() for ch in cleaned):
        return digits or cleaned

    return None


def parse_email(answer_text: str) -> Optional[str]:
    if not answer_text:
        return None

    email = answer_text.strip()
    if re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return email
    return None


def parse_preferences_priorities(answer_text: str) -> dict[str, int]:
    if not answer_text:
        return {}

    priorities: dict[str, int] = {}
    for match in PREFERENCE_PATTERN.finditer(answer_text):
        name = match.group("name").strip().lower()
        rating = int(match.group("rating"))
        normalized = PREFERENCE_NAME_MAP.get(name, PREFERENCE_NAME_MAP.get(name.lower()))
        if normalized and rating > 0:
            priorities[normalized] = rating

    return priorities
