from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.prescription import Prescription
from ..models.patient import Patient
from ..models.doctor import Doctor
from ..models.user import User
from pydantic import BaseModel

router = APIRouter()

class PrescriptionResponse(BaseModel):
    id: int
    patient_name: str
    doctor_name: str
    medication_name: str
    dosage: str
    frequency: str
    duration: str
    status: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[PrescriptionResponse])
async def get_prescriptions(db: Session = Depends(get_db)):
    prescriptions = db.query(Prescription).join(Patient).join(Doctor).all()
    
    result = []
    for prescription in prescriptions:
        result.append(PrescriptionResponse(
            id=prescription.id,
            patient_name=f"{prescription.patient.user.first_name} {prescription.patient.user.last_name}",
            doctor_name=f"Dr. {prescription.doctor.user.last_name}",
            medication_name=prescription.medication_name,
            dosage=prescription.dosage,
            frequency=prescription.frequency,
            duration=prescription.duration or "No especificado",
            status=prescription.status
        ))
    return result

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
async def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    return PrescriptionResponse(
        id=prescription.id,
        patient_name=f"{prescription.patient.user.first_name} {prescription.patient.user.last_name}",
        doctor_name=f"Dr. {prescription.doctor.user.last_name}",
        medication_name=prescription.medication_name,
        dosage=prescription.dosage,
        frequency=prescription.frequency,
        duration=prescription.duration or "No especificado",
        status=prescription.status
    )