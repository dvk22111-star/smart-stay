import os
import tempfile
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.dependencies import get_db
from price.price_calculator import (
    calculate_group_pricing,
    load_group_discount_rules,
)


class GroupPricingJsonRequest(BaseModel):
    group_id: int
    discount_rules: list[dict]


router = APIRouter(prefix="/price", tags=["Price"])


@router.post("/group-pricing/json")
def group_pricing_json(payload: GroupPricingJsonRequest, db: Session = Depends(get_db)):
    try:
        return calculate_group_pricing(db, payload.group_id, payload.discount_rules)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/group-pricing/excel")
async def group_pricing_excel(
    group_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    suffix = os.path.splitext(file.filename)[1] or ".xlsx"
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            discount_rules = load_group_discount_rules(tmp_path)
            return calculate_group_pricing(db, group_id, discount_rules)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
