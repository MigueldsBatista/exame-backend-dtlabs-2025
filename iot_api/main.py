from fastapi import FastAPI, Depends, HTTPException, status
from auth import User, get_password_hash, verify_password, create_access_token, decode_access_token, oauth2_scheme
from models.rest.post_reading import PostReading
from models.rest.get_reading import GetReading


app = FastAPI()

# Banco de dados simulado
fake_users_db = {}

# Endpoints
@app.post("/auth/register")
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe",
        )
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {"username": user.username, "password_hash": hashed_password}
    return {"msg": "Usuário registrado com sucesso"}

@app.post("/auth/login")
async def login(user: User):
    db_user = fake_users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Dependência para obter o usuário atual
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username

# Exemplo de endpoint protegido
#FIXME
@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}



@app.post("/data", response_model=PostReading, status_code=status.HTTP_201_CREATED)#response_model is used to return the data that was posted
async def register_reading(reading: PostReading):
    return reading

@app.get("/data", status_code=status.HTTP_200_OK)
async def get_reading(filter_query: GetReading = Depends()):
    return filter_query


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
#FIXME 