# verificar_pacientes.py
from app.database import get_db
from app.models.user import User
from app.models.patient import Patient

def main():
    db = next(get_db())
    
    print('=== VERIFICACIÓN FINAL ===')
    patients_data = db.query(User, Patient).outerjoin(Patient, User.id == Patient.user_id).filter(User.role == 'PATIENT').all()
    
    for user, patient in patients_data:
        print(f'Usuario: {user.email} -> Paciente ID: {patient.id if patient else "NO EXISTE"}')
    
    db.close()
    print('✅ Verificación completada!')

if __name__ == "__main__":
    main()