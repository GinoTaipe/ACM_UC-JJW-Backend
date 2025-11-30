from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base

print("=== INICIANDO SALUDCONECTADA API ===")

# IMPORTACIÓN DIRECTA Y SIMPLE - EVITAR __init__.py
from app.routes.auth import router as auth_router
from app.routes.patients import router as patients_router
from app.routes.doctors import router as doctors_router
from app.routes.medical_records import router as medical_records_router
from app.routes.prescriptions import router as prescriptions_router
from app.routes.appointments import router as appointments_router  # ESTA ES LA CLAVE

app = FastAPI(
    title="SaludConectada API",
    description="API para el sistema de gestión médica SaludConectada",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    print("Tablas de la base de datos creadas exitosamente!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "¡SaludConectada API está funcionando correctamente!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Sistema operativo"}

# REGISTRAR TODOS LOS ROUTERS
print("=== REGISTRANDO ROUTERS ===")

app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])
print("Auth router registrado")

app.include_router(patients_router, prefix="/api/patients", tags=["Pacientes"])
print("Patients router registrado")

app.include_router(doctors_router, prefix="/api/doctors", tags=["Médicos"])
print("Doctors router registrado")

app.include_router(medical_records_router, prefix="/api/medical-records", tags=["Historiales Médicos"])
print("Medical Records router registrado")

app.include_router(prescriptions_router, prefix="/api/prescriptions", tags=["Recetas"])
print("Prescriptions router registrado")

# APPOINTMENTS - EL IMPORTANTE
app.include_router(appointments_router, tags=["Citas"])
print("APPOINTMENTS ROUTER REGISTRADO EXITOSAMENTE!")
print(f"   - Prefix: {appointments_router.prefix}")
print(f"   - Tags: {appointments_router.tags}")

print("=== TODOS LOS ROUTERS REGISTRADOS ===")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )