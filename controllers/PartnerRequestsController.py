from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from dtos import PartnerRequestsDTO, PartnerRequestsCreateDTO#, PartnerRequestsUpdateDTO
from services.mapper.PartnerRequests import pr_service

router = APIRouter(prefix="/partner-requests", tags=["PartnerRequests"])


@router.get("/", response_model=list[PartnerRequestsDTO])
def get_all(db: Session = Depends(get_db)):
    return pr_service.get_all(db)


@router.get("/{id}", response_model=PartnerRequestsDTO)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return pr_service.get_by_id(db, id)


@router.post("/", response_model=PartnerRequestsDTO)
def create(payload: PartnerRequestsCreateDTO, db: Session = Depends(get_db)):
    return pr_service.create(db, payload)


#@router.put("/{id}", response_model=PartnerRequestsDTO)
#def update(id: int, payload: PartnerRequestsUpdateDTO, db: Session = Depends(get_db)):
#    return pr_service.update(db, id, payload)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return pr_service.delete(db, id)