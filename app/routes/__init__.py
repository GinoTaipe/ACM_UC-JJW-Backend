# Importar todas las rutas para facilitar el acceso
from .auth import router as auth_router
from .patients import router as patients_router
from .doctors import router as doctors_router
from .appointments import router as appointments_router
from .medical_records import router as medical_records_router
from .prescriptions import router as prescriptions_router

# Lista de todas las rutas disponibles
__all__ = [
    "auth_router",
    "patients_router", 
    "doctors_router",
    "appointments_router",
    "medical_records_router",
    "prescriptions_router"
]