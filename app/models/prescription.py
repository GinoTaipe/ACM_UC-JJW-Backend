from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    medical_record_id = Column(Integer, ForeignKey("medical_records.id"))
    medication_name = Column(String(200), nullable=False)
    dosage = Column(String(100), nullable=False)  # "500mg", "10ml"
    frequency = Column(String(100), nullable=False)  # "Cada 8 horas", "Una vez al día"
    duration = Column(String(100))  # "7 días", "Hasta terminar"
    instructions = Column(Text)  # Instrucciones adicionales
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    refills_available = Column(Integer, default=0)
    status = Column(String(20), default="active")  # active, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    patient = relationship("Patient", backref="prescriptions")
    doctor = relationship("Doctor", backref="prescriptions")
    # ✅ CAMBIO AQUÍ - backref único
    medical_record = relationship("MedicalRecord", backref="med_prescriptions")

    def __repr__(self):
        return f"<Prescription {self.medication_name} for Patient:{self.patient_id}>"