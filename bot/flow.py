from bot.parser import parse_preferences_priorities, parse_partner_request, parse_email


QUESTIONS = [
    {
        "id": "QUESTION_INTRO",
        "text": "היי! לפני שנתחיל, אני אשאל אותך כמה שאלות כדי לבנות את החדר המושלם עבורך. אחד = הכי חשוב, שניים = פחות חשוב, וכך הלאה.",
        "type": "info",
    },
    {
        "id": "QUESTION_PREFERENCES_OVERVIEW",
        "text": "אפשרויות ההעדפה הן: נוף לים, קומה נמוכה, קומה גבוהה.",
        "type": "info",
    },
    {
        "id": "QUESTION_PREFERENCE_PRIORITY",
        "text": "כתבי את ההעדפות שלך עם דירוגים: למשל 'נוף לים 1' ו'קומה נמוכה 2'. כל מספר ניתן פעם אחת בלבד.",
        "type": "preference_priority",
    },
    {
        "id": "QUESTION_SEA_VIEW_CONFIRM",
        "text": "נוף לים זמין בחדר זה בתוספת תשלום. האם תרצי להוסיף את הנוף? (כן/לא)",
        "type": "sea_view_confirm",
    },
    {
        "id": "QUESTION_PARTNER_REQUEST",
        "text": "האם יש לך חברה שתרצי להיות איתה בחדר? אם כן, כתבי את מספר הטלפון שלה בלבד. אם אין, כתבי 'לא'.",
        "type": "partner_request",
    },
    {
        "id": "QUESTION_EMAIL",
        "text": "אפשר לקבל את כתובת המייל שלך כדי שנוכל לשלוח אישור רישום?",
        "type": "email",
    },
    {
        "id": "QUESTION_COMPLETE",
        "text": "תודה רבה! סיימנו את איסוף הפרטים. אני שומר הכל וממשיך לשלב השיבוץ.",
        "type": "done",
    },
]


def get_question(question_id: str):
    if not question_id:
        return None
    for question in QUESTIONS:
        if question["id"] == question_id:
            return question
    return None


def next_question(current_question_id: str = None):
    if current_question_id is None:
        return QUESTIONS[0]
    for index, question in enumerate(QUESTIONS):
        if question["id"] == current_question_id:
            if index + 1 < len(QUESTIONS):
                return QUESTIONS[index + 1]
            return None
    return QUESTIONS[0]


def handle_answer(question_id: str, answer_text: str):
    if question_id in ("QUESTION_INTRO", "QUESTION_PREFERENCES_OVERVIEW"):
        return {
            "parsed": None,
            "next_question": next_question(question_id),
        }
    if question_id == "QUESTION_PREFERENCE_PRIORITY":
        priorities = parse_preferences_priorities(answer_text)
        return {
            "parsed": priorities,
            "next_question": "QUESTION_PARTNER_REQUEST",
        }
    if question_id == "QUESTION_PARTNER_REQUEST":
        partner_phone = parse_partner_request(answer_text)
        return {
            "parsed": partner_phone,
            "next_question": "QUESTION_EMAIL",
        }
    if question_id == "QUESTION_EMAIL":
        email = parse_email(answer_text)
        return {
            "parsed": email,
            "next_question": "QUESTION_COMPLETE",
        }
    return {
        "parsed": answer_text,
        "next_question": None,
    }
