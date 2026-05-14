import json
from models.partner_request import PartnerRequest

def load_partner_requests(path: str):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return [PartnerRequest(
        partner_request_id=item["PartnerRequestID"],
        member1_id=item["UserID1"],
        member2_id=item["UserID2"],
        vacation_id=item["VacationID"]
    ) for item in data]