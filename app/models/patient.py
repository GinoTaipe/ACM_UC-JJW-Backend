from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10))  # Male, Female, Other
    address = Column(Text)
    emergency_contact = Column(String(100))
    emergency_phone = Column(String(20))
    blood_type = Column(String(5))  # A+, O-, etc.
    allergies = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con el usuario
    user = relationship("User", backref="patient_profile")

    def __repr__(self):
        return f"<Patient {self.user.first_name} {self.user.last_name}>"