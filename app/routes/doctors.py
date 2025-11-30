from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.doctor import Doctor
from ..models.user import User
from pydantic import BaseModel

router = APIRouter()

class DoctorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    specialization: str
    license_number: str
    years_experience: int
    consultation_fee: int

    class Config:
        from_attributes = True

@router.get("/", response_model=List[DoctorResponse])
async def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).join(User).all()
    return doctors

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).join(User).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return doctor