# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database Configuration
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
    DB_NAME: str = os.getenv("DB_NAME", "SaludConectadaDB")
    
    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "tu_clave_secreta_super_segura_aqui_cambiar_por_una_muy_larga")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
    
    # Server Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8001"))

settings = Settings()