from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.patient import Patient
from ..models.user import User
from pydantic import BaseModel

router = APIRouter()

class PatientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: str
    gender: str
    blood_type: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[PatientResponse])
async def get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).join(User).all()
    return patients

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).join(User).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return patient