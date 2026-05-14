import json
from models.customer_preferences import CustomerPreference

def load_customer_preferences(path: str):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return [CustomerPreference(
        customer_pref_id=item["CustomerPreferencesID"],
        rating=item["Rating"],
        user_id=item["UserID"],
        preference_id=item["PreferencesID"],
        vacation_id=item["VacationID"]
    ) for item in data]