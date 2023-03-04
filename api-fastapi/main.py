from fastapi import FastAPI, Request, Response, Form
from model.handle_db import HandleDB
from controller.users import Users
from model.schemas import User
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users", tags=["users"])
def getUsers():
    try:
        db = HandleDB()
        users = db.get_users()
        print(users)
        return users
    except Exception as inst:
        print(inst)
        return {
            'message': str(inst),
            'error': True
        }


@app.post("/sign-up", tags=["users"])
def signUp(password: str = Form(), username: str = Form(), fullname: str = Form()):
    try:
        if len(username) < 4:
            raise Exception(
                "El nombre de usuario debe tener una longitud mayor a 4 caracteres")
        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            raise Exception("La contraseña no cumple los requisitos")
        if username and fullname and password:
            newUser = Users({
                'Username': username,
                'Fullname': fullname,
                'Password': password,
                'isAdmin': False,
            })
            userSaved = newUser.save()
            return userSaved
        else:
            return {
                "error": True,
                "message": "el nombre de usuario debe tener mas de 4 letras y la contraseña contener "
            }
    except Exception as inst:
        print(inst)
        return {
            'message': str(inst),
            'error': True
        }


@app.post("/sign-in", tags=["users"])
def signIn(password: str = Form(), username: str = Form()):
    try:
        print(password)
        db = HandleDB()
        isValid = db.validateUser(username, password)
        return isValid
    except Exception as inst:
        print(inst)
        return {
            'message': str(inst),
            'error': True
        }


@app.get("/artists", tags=['artists'])
def get_artists(search : str = ""):
    db = HandleDB()
    artists = db.get_artists(search)
    return artists


@app.delete("/artists/{id_artist}", tags=['artists'])
def delete_artist(id_artist: int):
    print(id_artist)
    db = HandleDB()
    artists = db.delete_artist(id_artist)
    print(artists)

    return {"error": "false", "message": "artist deleted"}


@app.post("/artists", tags=['artists'])
def create_or_update_artist(artistName: str, artistId : int = None):
    db = HandleDB()
    if(artistId):
        artist = artistId
        print(artistId, artistName)
        artist = db.edit_artist(artistName, artistId)
        return {"error": "false", "message": "artist edited", "artist": artist}
    else:
        artist = db.create_artist(artistName)
        return {"error": "false", "message": "artist created", "artist": artist}




