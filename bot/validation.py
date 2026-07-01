import re


def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email.strip()) is not None


def is_valid_phone(phone: str) -> bool:
    normalized = re.sub(r"[^0-9]", "", phone)
    return len(normalized) in (9, 10, 11) and normalized.startswith("0")


def is_valid_credit_card(card_number: str) -> bool:
    normalized = re.sub(r"[^0-9]", "", card_number)
    if len(normalized) < 13 or len(normalized) > 19:
        return False

    total = 0
    reverse_digits = normalized[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0
