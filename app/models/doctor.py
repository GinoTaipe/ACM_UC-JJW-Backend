from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    specialization = Column(String(100), nullable=False)
    years_experience = Column(Integer)
    education = Column(Text)
    bio = Column(Text)
    consultation_fee = Column(Integer)
    available_hours = Column(Text)  # JSON string con horarios
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    user = relationship("User", backref="doctor_profile")

    def __repr__(self):
        return f"<Doctor {self.user.first_name} {self.user.last_name} - {self.specialization}>"