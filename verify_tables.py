# backend/verify_tables.py
from app.database import engine
from sqlalchemy import text

def verify_database():
    with engine.connect() as conn:
        # Verificar base de datos
        result = conn.execute(text("SELECT DB_NAME()"))
        db_name = result.fetchone()
        print(f"📊 Base de datos actual: {db_name[0]}")
        
        # Verificar tablas
        result = conn.execute(text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """))
        tablas = [tabla[0] for tabla in result.fetchall()]
        print(f"📋 Tablas existentes: {tablas}")
        
        return tablas

if __name__ == "__main__":
    verify_database()