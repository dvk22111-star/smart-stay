from bot.parser import (
    parse_preferences_priorities,
    parse_partner_request,
    parse_email,
    parse_yes_no,
    parse_group_type,
    parse_integer,
    parse_phone_list,
    parse_credit_amount,
)


QUESTIONS = [
    {
        "id": "QUESTION_INTRO",
        "text": "היי! לפני שנתחיל, אני אשאל אותך כמה שאלות כדי לבנות את החדר המושלם עבורך.",
        "type": "info",
    },
    {
        "id": "QUESTION_NAME",
        "text": "איך קוראים לך?",
        "type": "name",
    },
    {
        "id": "QUESTION_EMAIL",
        "text": "אפשר לקבל את כתובת המייל שלך כדי שנוכל לשלוח אישור רישום?",
        "type": "email",
    },
    {
        "id": "QUESTION_GROUP_TYPE",
        "text": "האם זו הרשמה לקבוצה או אישית? כתבי 'קבוצה' או 'יחיד'.",
        "type": "group_type",
    },
    {
        "id": "QUESTION_GROUP_NAME",
        "text": "מה שם הקבוצה?",
        "type": "group_name",
    },
    {
        "id": "QUESTION_GROUP_SIZE",
        "text": "כמה משתתפים יהיו בקבוצה?",
        "type": "group_size",
    },
    {
        "id": "QUESTION_GROUP_PAYMENT_TYPE",
        "text": "האם התשלום הוא כוללני לכל החברים? כתבי 'כן' או 'לא'.",
        "type": "group_payment",
    },
    {
        "id": "QUESTION_GROUP_MEMBER_PHONES",
        "text": "אנא שלחי את מספרי הטלפון של חברי הקבוצה, מופרדים בפסיקים.",
        "type": "group_members",
    },
    {
        "id": "QUESTION_PREFERENCES_OVERVIEW",
        "text": "עכשיו נבחר את ההעדפות. כל העדפה יכולה להיבחר פעם אחת בלבד ולדרג מ-1 עד מספר האפשרויות.",
        "type": "info",
    },
    {
        "id": "QUESTION_PREFERENCE_PRIORITY",
        "text": "כתבי את ההעדפות שלך עם דירוגים: למשל 'נוף לים 1' ו'קומה נמוכה 2'. כל מספר ניתן פעם אחת בלבד.",
        "type": "preference_priority",
    },
    {
        "id": "QUESTION_PARTNER_REQUEST",
        "text": "האם יש לך חברה שתרצי להיות איתה בחדר? כתבי את מספר הטלפון שלה או 'לא'.",
        "type": "partner_request",
    },
    {
        "id": "QUESTION_CREDIT_AMOUNT",
        "text": "כמה סכום אשראי תרצי להקצות כרגע לרישום זה?",
        "type": "credit_amount",
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
    if question_id == "QUESTION_NAME":
        return {
            "parsed": answer_text.strip() if answer_text else None,
            "next_question": "QUESTION_EMAIL",
        }
    if question_id == "QUESTION_EMAIL":
        email = parse_email(answer_text)
        return {
            "parsed": email,
            "next_question": "QUESTION_GROUP_TYPE",
        }
    if question_id == "QUESTION_GROUP_TYPE":
        group_type = parse_group_type(answer_text)
        next_q = "QUESTION_GROUP_NAME" if group_type == "group" else "QUESTION_PREFERENCES_OVERVIEW"
        return {
            "parsed": group_type,
            "next_question": next_q,
        }
    if question_id == "QUESTION_GROUP_NAME":
        return {
            "parsed": answer_text.strip() if answer_text else None,
            "next_question": "QUESTION_GROUP_SIZE",
        }
    if question_id == "QUESTION_GROUP_SIZE":
        group_size = parse_integer(answer_text)
        return {
            "parsed": group_size,
            "next_question": "QUESTION_GROUP_PAYMENT_TYPE",
        }
    if question_id == "QUESTION_GROUP_PAYMENT_TYPE":
        paid_as_group = parse_yes_no(answer_text)
        return {
            "parsed": paid_as_group,
            "next_question": "QUESTION_GROUP_MEMBER_PHONES",
        }
    if question_id == "QUESTION_GROUP_MEMBER_PHONES":
        members = parse_phone_list(answer_text)
        return {
            "parsed": members,
            "next_question": "QUESTION_PREFERENCES_OVERVIEW",
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
            "next_question": "QUESTION_CREDIT_AMOUNT",
        }
    if question_id == "QUESTION_CREDIT_AMOUNT":
        amount = parse_credit_amount(answer_text)
        return {
            "parsed": amount,
            "next_question": "QUESTION_COMPLETE",
        }
    return {
        "parsed": answer_text,
        "next_question": None,
    }
