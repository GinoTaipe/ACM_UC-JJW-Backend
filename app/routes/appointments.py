from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.appointment import Appointment, AppointmentStatus
from ..models.patient import Patient
from ..models.doctor import Doctor
from ..models.user import User
from pydantic import BaseModel
from datetime import datetime

# ✅ CORREGIDO: Agregar prefix aquí
router = APIRouter(prefix="/api/appointments", tags=["Citas"])

# 🆕 MODELO PARA CREAR CITA
class CreateAppointmentRequest(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    reason: str = "Consulta general"

class AppointmentResponse(BaseModel):
    id: int
    patient_name: str
    patient_id: int  # 🆕 NUEVA LINEA
    doctor_name: str
    appointment_date: datetime
    duration_minutes: int  # 🆕 NUEVA LINEA
    status: str
    reason: str

    class Config:
        from_attributes = True

# ✅ CORREGIDO: Función create_appointment simplificada y funcional
@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment_data: CreateAppointmentRequest, 
    db: Session = Depends(get_db)
):
    try:
        print(f"🔍 DEBUG: Recibiendo cita - patient_id: {appointment_data.patient_id}, doctor_id: {appointment_data.doctor_id}")
        
        # Verificar que el paciente existe
        patient = db.query(Patient).filter(Patient.id == appointment_data.patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        # Obtener usuario del paciente por separado
        patient_user = db.query(User).filter(User.id == patient.user_id).first()
        if not patient_user:
            raise HTTPException(status_code=404, detail="Usuario del paciente no encontrado")
        
        # Verificar que el médico existe
        doctor = db.query(Doctor).filter(Doctor.id == appointment_data.doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        
        # Obtener usuario del médico por separado
        doctor_user = db.query(User).filter(User.id == doctor.user_id).first()
        if not doctor_user:
            raise HTTPException(status_code=404, detail="Usuario del médico no encontrado")
        
        print(f"🔍 DEBUG: Paciente user: {patient_user.first_name} {patient_user.last_name}")
        print(f"🔍 DEBUG: Médico user: {doctor_user.first_name} {doctor_user.last_name}")
        
        # Crear nueva cita
        new_appointment = Appointment(
            patient_id=appointment_data.patient_id,
            doctor_id=appointment_data.doctor_id,
            appointment_date=appointment_data.appointment_date,
            reason=appointment_data.reason,
            status=AppointmentStatus.SCHEDULED
        )
        
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        
        print(f"🎉 CITA CREADA EXITOSAMENTE - ID: {new_appointment.id}")
        
        # Retornar la respuesta
        return AppointmentResponse(
    id=new_appointment.id,
    patient_name=f"{patient_user.first_name} {patient_user.last_name}",
    patient_id=appointment_data.patient_id,  # 🆕 NUEVA LINEA
    doctor_name=f"Dr. {doctor_user.last_name}",
    appointment_date=new_appointment.appointment_date,
    duration_minutes=new_appointment.duration_minutes or 30,  # 🆕 NUEVA LINEA
    status=new_appointment.status.value,
    reason=new_appointment.reason
)
        
    except Exception as e:
        db.rollback()
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al crear la cita: {str(e)}")

# 🆕 ENDPOINT PARA CITAS DE PACIENTE
@router.get("/patient/{patient_id}", response_model=List[AppointmentResponse])
async def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.patient_id == patient_id).all()
    
    result = []
    for appointment in appointments:
        # Obtener información de usuario para cada cita
        patient_user = db.query(User).filter(User.id == appointment.patient.user_id).first()
        doctor_user = db.query(User).filter(User.id == appointment.doctor.user_id).first()
        
        result.append(AppointmentResponse(
            id=appointment.id,
            patient_name=f"{patient_user.first_name} {patient_user.last_name}",
            doctor_name=f"Dr. {doctor_user.last_name}",
            appointment_date=appointment.appointment_date,
            status=appointment.status.value,
            reason=appointment.reason or "Consulta general"
        ))
    return result

# 🆕 ENDPOINT PARA CITAS DE MÉDICO
@router.get("/doctor/{doctor_id}", response_model=List[AppointmentResponse])
async def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()
    
    result = []
    for appointment in appointments:
        # Obtener información de usuario para cada cita
        patient_user = db.query(User).filter(User.id == appointment.patient.user_id).first()
        doctor_user = db.query(User).filter(User.id == appointment.doctor.user_id).first()
        
        result.append(AppointmentResponse(
    id=appointment.id,
    patient_name=f"{patient_user.first_name} {patient_user.last_name}",
    patient_id=appointment.patient_id,  # 🆕 NUEVA LINEA
    doctor_name=f"Dr. {doctor_user.last_name}",
    appointment_date=appointment.appointment_date,
    duration_minutes=appointment.duration_minutes or 30,  # 🆕 NUEVA LINEA
    status=appointment.status.value,
    reason=appointment.reason or "Consulta general"
))
    return result

# 🆕 ENDPOINT PARA HORARIOS DISPONIBLES
@router.get("/doctor/{doctor_id}/available-slots")
async def get_available_slots(doctor_id: int, date: str, db: Session = Depends(get_db)):
    """
    Obtener horarios disponibles de un médico en una fecha específica
    """
    try:
        # Verificar que el médico existe
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        
        # Por simplicidad, retornamos horarios fijos para testing
        # En producción, aquí consultarías la base de datos por citas existentes
        available_slots = [
            "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
            "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
        ]
        return available_slots
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener horarios: {str(e)}")

# TUS ENDPOINTS EXISTENTES SE MANTIENEN
@router.get("/", response_model=List[AppointmentResponse])
async def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    
    result = []
    for appointment in appointments:
        # Obtener información de usuario para cada cita
        patient_user = db.query(User).filter(User.id == appointment.patient.user_id).first()
        doctor_user = db.query(User).filter(User.id == appointment.doctor.user_id).first()
        
        result.append(AppointmentResponse(
            id=appointment.id,
            patient_name=f"{patient_user.first_name} {patient_user.last_name}",
            doctor_name=f"Dr. {doctor_user.last_name}",
            appointment_date=appointment.appointment_date,
            status=appointment.status.value,
            reason=appointment.reason or "Consulta general"
        ))
    return result

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    # Obtener información de usuario
    patient_user = db.query(User).filter(User.id == appointment.patient.user_id).first()
    doctor_user = db.query(User).filter(User.id == appointment.doctor.user_id).first()
    
    return AppointmentResponse(
        id=appointment.id,
        patient_name=f"{patient_user.first_name} {patient_user.last_name}",
        doctor_name=f"Dr. {doctor_user.last_name}",
        appointment_date=appointment.appointment_date,
        status=appointment.status.value,
        reason=appointment.reason or "Consulta general"
    )