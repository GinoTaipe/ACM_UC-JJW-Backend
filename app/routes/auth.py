from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from pydantic import BaseModel, validator
from ..models.user import UserRole
import secrets

# ✅ ESTA LÍNEA ES CRÍTICA - DEFINE EL ROUTER
router = APIRouter()

class LoginRequest(BaseModel):
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str
    first_name: str
    last_name: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str
    role: UserRole

    @validator('password')
    def validate_password(cls, v):
        if len(v) > 72:
            raise ValueError('La contraseña no puede tener más de 72 caracteres')
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v

@router.post("/register", response_model=Token)
async def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        print("🔍 [DEBUG] Iniciando proceso de registro...")
        print(f"🔍 [DEBUG] Datos recibidos: {register_data}")
        
        # Verificar si el usuario ya existe
        print("🔍 [DEBUG] Verificando si el usuario existe...")
        existing_user = db.query(User).filter(User.email == register_data.email).first()
        if existing_user:
            print("❌ [DEBUG] El email ya está registrado")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )

        print("🔍 [DEBUG] Creando objeto User...")
        # Crear nuevo usuario
        new_user = User(
            email=register_data.email,
            password_hash=register_data.password,
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            phone=register_data.phone,
            role=register_data.role,
            is_active=True
        )
        print(f"🔍 [DEBUG] Usuario creado: {new_user}")
        
        print("🔍 [DEBUG] Guardando en base de datos...")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"🔍 [DEBUG] Usuario guardado con ID: {new_user.id}")
        
        print("🔍 [DEBUG] Creando token JWT...")
        # Crear token de acceso simple (para demo)
        access_token = secrets.token_urlsafe(32)

        print("✅ [DEBUG] Registro completado exitosamente")
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=new_user.id,
            role=new_user.role.value,
            first_name=new_user.first_name,
            last_name=new_user.last_name
        )
        
    except Exception as e:
        print(f"❌ [DEBUG ERROR]: {str(e)}")
        print(f"❌ [DEBUG ERROR TYPE]: {type(e)}")
        import traceback
        print(f"❌ [DEBUG TRACEBACK]: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )

    # Crear token de acceso simple (para demo)
    access_token = secrets.token_urlsafe(32)

    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        role=user.role.value,
        first_name=user.first_name,
        last_name=user.last_name
    )