# crear_medicos.py
from app.database import get_db
from app.models.doctor import Doctor
import datetime

def main():
    db = next(get_db())
    
    print('=== CREANDO REGISTROS DE MÉDICOS FALTANTES ===')
    
    # Lista de usuarios doctor que necesitan registro en tabla doctors
    doctor_users = [
        {'user_id': 2, 'email': 'doctor@saludconectada.com', 'name': 'Carlos Rodríguez', 'specialization': 'Cardiología'},
        {'user_id': 4, 'email': 'Walter123@saludconectada.com', 'name': 'Walter Torres', 'specialization': 'Pediatría'}
    ]
    
    for user_data in doctor_users:
        # Verificar si ya existe
        existing = db.query(Doctor).filter(Doctor.user_id == user_data['user_id']).first()
        if not existing:
            new_doctor = Doctor(
                user_id=user_data['user_id'],
                license_number=f"LIC-{user_data['user_id']}123",
                specialization=user_data['specialization'],
                years_experience=5,
                education="Universidad de Medicina",
                bio=f"Médico especialista en {user_data['specialization']}",
                consultation_fee=80.00,
                available_hours="Lunes a Viernes: 8:00 - 16:00",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db.add(new_doctor)
            print(f'✅ Creado médico para usuario: {user_data["email"]} (User ID: {user_data["user_id"]}) - {user_data["specialization"]}')
        else:
            print(f'⚠️  Ya existe médico para: {user_data["email"]}')
    
    db.commit()
    
    print('=== VERIFICANDO REGISTROS CREADOS ===')
    doctors = db.query(Doctor).all()
    for d in doctors:
        print(f'🩺 Médico ID: {d.id} -> User ID: {d.user_id} -> Especialización: {d.specialization}')
    
    db.close()
    print('🎉 MÉDICOS CREADOS EXITOSAMENTE!')

if __name__ == "__main__":
    main()