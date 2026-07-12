import pandas as pd
from sqlalchemy.orm import Session

from models import (
    Vacation,
    CustomerPreferences,
    PreferencePrice,
    Group,
    VacationersCustomers,
)


def load_group_discount_rules(excel_path: str, sheet_name: str | None = None) -> list[dict]:
    """Load group discount rules from an Excel file.

    The Excel file should contain a table with a minimum group size,
    a maximum group size, and a discount value. Discount can be numeric
    (fixed amount) or a percentage string like '10%'.
    """
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    df.columns = [str(col).strip().lower() for col in df.columns]

    if "min_size" in df.columns:
        min_col = "min_size"
    elif "min_count" in df.columns:
        min_col = "min_count"
    elif "minimum" in df.columns:
        min_col = "minimum"
    else:
        raise ValueError("Excel must contain a minimum group size column")

    if "max_size" in df.columns:
        max_col = "max_size"
    elif "max_count" in df.columns:
        max_col = "max_count"
    elif "maximum" in df.columns:
        max_col = "maximum"
    else:
        raise ValueError("Excel must contain a maximum group size column")

    if "discount" in df.columns:
        discount_col = "discount"
    elif "discount_amount" in df.columns:
        discount_col = "discount_amount"
    elif "discount_percent" in df.columns:
        discount_col = "discount_percent"
    else:
        raise ValueError("Excel must contain a discount column")

    rules = []
    for _, row in df.iterrows():
        min_size = int(row[min_col])
        max_size = int(row[max_col])
        discount = row[discount_col]

        if isinstance(discount, str):
            discount = discount.strip()
            if discount.endswith("%"):
                rules.append({
                    "min_size": min_size,
                    "max_size": max_size,
                    "discount": discount,
                })
                continue
            discount = discount.replace("₪", "").strip()
            discount = float(discount) if discount != "" else 0.0
        elif pd.isna(discount):
            discount = 0.0

        rules.append({
            "min_size": min_size,
            "max_size": max_size,
            "discount": float(discount),
        })

    rules.sort(key=lambda item: item["min_size"])
    return rules


def get_preference_extra_for_user(db: Session, user_id: int, vacation_id: int) -> float:
    """Return the additional price for the user's preference on a vacation."""
    pref = (
        db.query(CustomerPreferences)
        .filter(
            CustomerPreferences.UserID == user_id,
            CustomerPreferences.VacationID == vacation_id,
        )
        .first()
    )
    if not pref:
        return 0.0

    price_item = (
        db.query(PreferencePrice)
        .filter(PreferencePrice.PreferenceID == pref.PreferencesID)
        .first()
    )
    return float(price_item.AdditionalPrice) if price_item else 0.0


def calculate_individual_price(db: Session, user_id: int, vacation_id: int) -> float:
    """Calculate base price plus preference extra for a single user not in a group."""
    vacation = db.query(Vacation).filter(Vacation.VacationID == vacation_id).first()
    if not vacation:
        raise ValueError("Vacation not found")

    base_price = float(vacation.BasicCost)
    extra = get_preference_extra_for_user(db, user_id, vacation_id)
    return base_price + extra


def find_discount_for_group(group_size: int, discount_rules: list[dict]) -> float:
    """Return discount amount or percent for a group based on rules."""
    for rule in discount_rules:
        min_size = rule.get("min_size")
        max_size = rule.get("max_size")
        discount = rule.get("discount")
        if min_size <= group_size <= max_size:
            return discount
    return 0.0


def calculate_group_total(
    base_price: float,
    group_size: int,
    discount_rules: list[dict],
) -> float:
    """Calculate total group price after applying group discount."""
    discount = find_discount_for_group(group_size, discount_rules)
    if not discount:
        return base_price * group_size

    if isinstance(discount, str) and discount.endswith("%"):
        percent = float(discount.strip("%")) / 100.0
        return base_price * group_size * (1 - percent)

    return max(0.0, base_price * group_size - float(discount))


def calculate_group_member_price(
    total_price: float,
    group_size: int,
    preference_extra: float = 0.0,
) -> float:
    """Calculate per-member price for a group member, including only that member's preference extra."""
    if group_size <= 0:
        raise ValueError("Group size must be positive")

    shared_base = total_price / group_size
    return shared_base + preference_extra


def calculate_group_pricing(
    db: Session,
    group_id: int,
    discount_rules: list[dict],
) -> dict:
    """Calculate pricing for an entire group and its individual members."""
    group = db.query(Group).filter(Group.GroupID == group_id).first()
    if not group:
        raise ValueError("Group not found")

    vacation = db.query(Vacation).filter(Vacation.VacationID == group.VacationID).first()
    if not vacation:
        raise ValueError("Vacation not found")

    group_size = group.NumberofParticipants or 0
    base_price = float(vacation.BasicCost)
    total_price = calculate_group_total(base_price, group_size, discount_rules)

    members = (
        db.query(VacationersCustomers)
        .filter(VacationersCustomers.VacationID == group.VacationID)
        .all()
    )

    member_prices = []
    for member in members:
        if member.GroupMemberNumber is None:
            continue
        extra = get_preference_extra_for_user(db, member.UserID, group.VacationID)
        member_price = calculate_group_member_price(total_price, group_size, extra)
        member_prices.append(
            {
                "VacationIDForCustomers": member.VacationIDForCustomers,
                "UserID": member.UserID,
                "GroupMemberNumber": member.GroupMemberNumber,
                "PreferenceExtra": extra,
                "Price": member_price,
            }
        )

    return {
        "GroupID": group.GroupID,
        "VacationID": group.VacationID,
        "GroupSize": group_size,
        "BasePrice": base_price,
        "TotalPrice": total_price,
        "MemberPrices": member_prices,
    }


def calculate_group_pricing_from_excel(
    db: Session,
    group_id: int,
    excel_path: str,
    sheet_name: str | None = None,
) -> dict:
    """Calculate group pricing directly from an Excel discount file."""
    discount_rules = load_group_discount_rules(excel_path, sheet_name=sheet_name)
    return calculate_group_pricing(db, group_id, discount_rules)
