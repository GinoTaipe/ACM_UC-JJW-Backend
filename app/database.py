# backend/app/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Conexión inicial a master para crear la base de datos si no existe
master_connection_string = (
    "mssql+pyodbc://localhost\\SQLEXPRESS/master"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

# Conexión a la base de datos de la aplicación
app_connection_string = (
    f"mssql+pyodbc://localhost\\SQLEXPRESS/{settings.DB_NAME}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

def create_database_if_not_exists():
    """Crear la base de datos si no existe"""
    try:
        # Conectar a master con autocommit
        master_engine = create_engine(master_connection_string, connect_args={"timeout": 10}, isolation_level="AUTOCOMMIT")
        with master_engine.connect() as conn:
            # Verificar si la base de datos existe
            result = conn.execute(text(f"SELECT name FROM sys.databases WHERE name = '{settings.DB_NAME}'"))
            if not result.fetchone():
                print(f"Creando base de datos {settings.DB_NAME}...")
                conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
                print(f"Base de datos {settings.DB_NAME} creada exitosamente!")
            else:
                print(f"Base de datos {settings.DB_NAME} ya existe.")
        master_engine.dispose()
    except Exception as e:
        print(f"Error al crear/verificar base de datos: {e}")
        raise

# Crear la base de datos si no existe
create_database_if_not_exists()

# Crear engine de conexión a la base de datos de la aplicación
engine = create_engine(
    app_connection_string,
    pool_pre_ping=True,
    echo=True,  # Muestra las queries en consola
    connect_args={"timeout": 10}
)

# Session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()