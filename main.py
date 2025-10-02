from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API de Usuarios CRUD")

# Modelos de datos
class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    is_active: bool = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    is_active: bool

class LoginRequest(BaseModel):
    username: str
    password: str

# Base de datos en memoria
users_db = []
next_id = 1

# CREAR usuario
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    global next_id
    
    # Verificar si el usuario ya existe
    for u in users_db:
        if u["username"] == user.username:
            raise HTTPException(400, "Usuario ya existe")
    
    nuevo_usuario = {
        "id": next_id,
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "is_active": user.is_active
    }
    
    users_db.append(nuevo_usuario)
    next_id += 1
    
    return {
        "id": nuevo_usuario["id"],
        "username": nuevo_usuario["username"],
        "email": nuevo_usuario["email"],
        "is_active": nuevo_usuario["is_active"]
    }

# LISTAR todos los usuarios
@app.get("/users", response_model=List[UserResponse])
def get_all_users():
    respuesta = []
    for user in users_db:
        respuesta.append({
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "is_active": user["is_active"]
        })
    return respuesta

# OBTENER un usuario por ID
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "is_active": user["is_active"]
            }
    raise HTTPException(404, "Usuario no encontrado")

# ACTUALIZAR usuario (sin cambiar password)
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserCreate):
    for user in users_db:
        if user["id"] == user_id:
            # Verificar que el nuevo username no exista
            for u in users_db:
                if u["username"] == user_data.username and u["id"] != user_id:
                    raise HTTPException(400, "Username ya existe")
            
            user["username"] = user_data.username
            user["email"] = user_data.email
            user["is_active"] = user_data.is_active
            
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "is_active": user["is_active"]
            }
    
    raise HTTPException(404, "Usuario no encontrado")

# ELIMINAR usuario
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users_db
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db.pop(i)
            return {"message": "Usuario eliminado"}
    raise HTTPException(404, "Usuario no encontrado")

# LOGIN
@app.post("/login")
def login(login_data: LoginRequest):
    for user in users_db:
        if user["username"] == login_data.username and user["password"] == login_data.password:
            return {"message": "Login exitoso"}
    return {"message": "Login fallido"}

# Crear usuarios de ejemplo al iniciar
@app.on_event("startup")
def crear_usuarios_ejemplo():
    usuarios_ejemplo = [
        {"username": "Camila", "password": "A1", "email": "camila@ejemplo.com"},
        {"username": "Matias", "password": "B2", "email": "matias@ejemplo.com"},
        {"username": "Valeria", "password": "C3", "email": "valeria@ejemplo.com"},
        {"username": "Milena", "password": "a1", "email": "milena@ejemplo.com"},
        {"username": "Angelica", "password": "b2", "email": "angelica@ejemplo.com"}
    ]
    
    for usuario in usuarios_ejemplo:
        create_user(UserCreate(**usuario))

# Ruta de prueba
@app.get("/")
def home():
    return {"message": "API CRUD de Usuarios funcionando"}
