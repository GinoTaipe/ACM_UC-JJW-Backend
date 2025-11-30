import re
from datetime import datetime

def is_valid_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    """Valida formato de teléfono"""
    pattern = r'^[\+]?[0-9\s\-\(\)]{7,15}$'
    return re.match(pattern, phone) is not None

def is_valid_date(date_string: str) -> bool:
    """Valida formato de fecha YYYY-MM-DD"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_password(password: str) -> bool:
    """Valida fortaleza de contraseña"""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True