# check_users.py
import pyodbc
from app.database import get_db
from app.models.user import User

db = next(get_db())
users = db.query(User).all()

for user in users:
    print(f"ID: {user.id}, Email: {user.email}, Nombre: {user.first_name} {user.last_name}, Rol: {user.role}")