from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    record_date = Column(DateTime, nullable=False)
    height = Column(Float)  # en cm
    weight = Column(Float)  # en kg
    blood_pressure = Column(String(20))  # "120/80"
    heart_rate = Column(Integer)  # pulsaciones por minuto
    temperature = Column(Float)  # en Celsius
    symptoms = Column(Text)
    diagnosis = Column(Text)
    treatment = Column(Text)
    prescriptions = Column(Text)  # JSON con medicamentos
    notes = Column(Text)
    follow_up_required = Column(String, default=False)
    follow_up_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    patient = relationship("Patient", backref="medical_records")
    doctor = relationship("Doctor", backref="medical_records")
    appointment = relationship("Appointment", backref="medical_record")

    def __repr__(self):
        return f"<MedicalRecord Patient:{self.patient_id} Date:{self.record_date}>"