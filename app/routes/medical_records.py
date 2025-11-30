from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.medical_record import MedicalRecord
from ..models.patient import Patient
from ..models.doctor import Doctor
from ..models.user import User
from pydantic import BaseModel

router = APIRouter()

class MedicalRecordResponse(BaseModel):
    id: int
    patient_name: str
    doctor_name: str
    record_date: str
    diagnosis: str
    treatment: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[MedicalRecordResponse])
async def get_medical_records(db: Session = Depends(get_db)):
    records = db.query(MedicalRecord).join(Patient).join(Doctor).all()
    
    result = []
    for record in records:
        result.append(MedicalRecordResponse(
            id=record.id,
            patient_name=f"{record.patient.user.first_name} {record.patient.user.last_name}",
            doctor_name=f"Dr. {record.doctor.user.last_name}",
            record_date=record.record_date.strftime("%Y-%m-%d"),
            diagnosis=record.diagnosis or "Sin diagnóstico",
            treatment=record.treatment or "Sin tratamiento"
        ))
    return result

@router.get("/{record_id}", response_model=MedicalRecordResponse)
async def get_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Historial médico no encontrado")
    
    return MedicalRecordResponse(
        id=record.id,
        patient_name=f"{record.patient.user.first_name} {record.patient.user.last_name}",
        doctor_name=f"Dr. {record.doctor.user.last_name}",
        record_date=record.record_date.strftime("%Y-%m-%d"),
        diagnosis=record.diagnosis or "Sin diagnóstico",
        treatment=record.treatment or "Sin tratamiento"
    )