# verificar_medicos.py
from app.database import get_db
from app.models.user import User
from app.models.doctor import Doctor

def main():
    db = next(get_db())
    
    print('=== VERIFICACIÓN MÉDICOS ===')
    doctors_data = db.query(User, Doctor).outerjoin(Doctor, User.id == Doctor.user_id).filter(User.role == 'DOCTOR').all()
    
    for user, doctor in doctors_data:
        print(f'Usuario: {user.email} -> Médico ID: {doctor.id if doctor else "NO EXISTE"} -> Especialización: {doctor.specialization if doctor else "N/A"}')
    
    db.close()
    print('✅ Verificación médicos completada!')

if __name__ == "__main__":
    main()