# crear_pacientes.py
from app.database import get_db
from app.models.patient import Patient
import datetime

def main():
    db = next(get_db())
    
    print('=== CREANDO REGISTROS DE PACIENTES FALTANTES ===')
    
    # Lista de usuarios paciente que necesitan registro en tabla patients
    patient_users = [
        {'user_id': 1, 'email': 'paciente@saludconectada.com'},
        {'user_id': 5, 'email': 'Quispe@saludconectada.com'},
        {'user_id': 6, 'email': 'jarm@saludconectada.com'}
    ]
    
    for user_data in patient_users:
        # Verificar si ya existe
        existing = db.query(Patient).filter(Patient.user_id == user_data['user_id']).first()
        if not existing:
            new_patient = Patient(
                user_id=user_data['user_id'],
                date_of_birth=datetime.date(1990, 1, 1),
                gender='Masculino',
                address='Dirección de prueba 123',
                emergency_contact='Contacto emergencia',
                emergency_phone='123456789',
                blood_type='O+',
                allergies='Ninguna',
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db.add(new_patient)
            print(f'✅ Creado paciente para usuario: {user_data["email"]} (User ID: {user_data["user_id"]})')
        else:
            print(f'⚠️  Ya existe paciente para: {user_data["email"]}')
    
    db.commit()
    
    print('=== VERIFICANDO REGISTROS CREADOS ===')
    patients = db.query(Patient).all()
    for p in patients:
        print(f'📋 Paciente ID: {p.id} -> User ID: {p.user_id}')
    
    db.close()
    print('🎉 PROCESO COMPLETADO!')

if __name__ == "__main__":
    main()