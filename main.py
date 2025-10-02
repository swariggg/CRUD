from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
app = FastAPI(title="CRUD")
class Login(BaseModel):
    correo: str
    password: str
class UsuarioNuevo(BaseModel):
    usuario: str
    correo: str
    password: str
    activa: Optional[bool] = True
class SalidaUsuario(BaseModel):
    id: int
    usuario: str
    correo: str
    activa: bool
usuarios = [
    {"id": 1, "usuario": "Camila", "correo": "camilasolvil@gmail.com", "password": "ABC2024", "activa": True},
    {"id": 2, "usuario": "Matias",  "correo": "matias090@gmail.com", "password": "Pass09", "activa": True},
    {"id": 3, "usuario": "Valeria", "correo": "valelemus@gmail.com", "password": "AjIplj0", "activa": True},
    {"id": 4, "usuario": "Milena",  "correo": "milevilla.com", "password": "Abyss98", "activa": True},
    {"id": 5, "usuario": "Angelica",  "correo": "angiefelton@gmail.com", "password": "bohemian", "activa": True}
]
@app.post("/usuarios", response_model=SalidaUsuario, status_code=201)
def crear_usuario(u: UsuarioNuevo):
    if any(x["correo"] == u.correo for x in usuarios):
        raise HTTPException(status_code=400, detail="correo ya existente")
    nuevo_id = max((x["id"] for x in usuarios), default=0) + 1
    user = {
        "id": nuevo_id,
        "usuario": u.usuario,
        "correo": u.correo,
        "password": u.password,
        "activa": u.activa
    }
    usuarios.append(user)
    return {"id": user["id"], "usuario": user["usuario"], "correo": user["correo"], "activa": user["activa"]}
@app.get("/usuarios", response_model=List[SalidaUsuario])
def listar_usuarios():
    return [{"id": x["id"], "usuario": x["usuario"], "correo": x["correo"], "activa": x["activa"]} for x in usuarios]
@app.get("/usuarios/{user_id}", response_model=SalidaUsuario)
def obtener_usuario(user_id: int):
    u = next((x for x in usuarios if x["id"] == user_id), None)
    if not u:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return {"id": u["id"], "usuario": u["usuario"], "correo": u["correo"], "activa": u["activa"]}
@app.put("/usuarios/{user_id}", response_model=SalidaUsuario)
def actualizar_usuario(user_id: int, data: UsuarioNuevo):
    u = next((x for x in usuarios if x["id"] == user_id), None)
    if not u:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    if any(x["correo"] == data.correo and x["id"] != user_id for x in usuarios):
        raise HTTPException(status_code=400, detail="correo ya en uso por otro usuario")
    u["usuario"] = data.usuario
    u["correo"] = data.correo
    u["password"] = data.password
    u["activa"] = data.activa if data.activa is not None else u["activa"]
    return {"id": u["id"], "usuario": u["usuario"], "correo": u["correo"], "activa": u["activa"]}
@app.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: int):
    global usuarios
    if not any(x["id"] == user_id for x in usuarios):
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    usuarios = [x for x in usuarios if x["id"] != user_id]
    return {"message": "Usuario eliminado"}
@app.post("/login")
def login(payload: Login):
    user = next((x for x in usuarios if x["correo"] == payload.correo and x["password"] == payload.password), None)
    if user:
        return {"message": "Login exitoso"}
    return {"message": "Credenciales inválidas"}
