# create_test_users.py
from app.database import get_db
from app.models.user import User, UserRole

def main():
    db = next(get_db())

    print('=== CREANDO USUARIOS DE PRUEBA ===')

    # Test users
    test_users = [
        {
            'email': 'paciente@saludconectada.com',
            'password': 'test123',
            'first_name': 'Juan',
            'last_name': 'Perez',
            'phone': '123456789',
            'role': UserRole.PATIENT
        },
        {
            'email': 'doctor@saludconectada.com',
            'password': 'test123',
            'first_name': 'Maria',
            'last_name': 'Garcia',
            'phone': '987654321',
            'role': UserRole.DOCTOR
        },
        {
            'email': 'admin@saludconectada.com',
            'password': 'test123',
            'first_name': 'Admin',
            'last_name': 'Sistema',
            'phone': '555555555',
            'role': UserRole.ADMIN
        }
    ]

    for user_data in test_users:
        # Check if user already exists
        existing = db.query(User).filter(User.email == user_data['email']).first()
        if not existing:
            new_user = User(
                email=user_data['email'],
                password_hash=user_data['password'],  # Note: in production this should be hashed
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                role=user_data['role'],
                is_active=True
            )
            db.add(new_user)
            print(f'Created user: {user_data["email"]}')
        else:
            print(f'User already exists: {user_data["email"]}')

    db.commit()

    # Verify users were created
    print('\n=== VERIFICANDO USUARIOS CREADOS ===')
    users = db.query(User).all()
    for user in users:
        print(f'ID: {user.id}, Email: {user.email}, Role: {user.role.value}, Active: {user.is_active}')

    db.close()
    print('Done!')

if __name__ == "__main__":
    main()