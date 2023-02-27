from fastapi import FastAPI, Request, Response, Form
from model.handle_db import HandleDB
from controller.users import Users
from model.schemas import User


app = FastAPI()


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
def signUp(password: str = Form(), username: str = Form(), fullname : str = Form()):
    try:
        newUser = Users( {
            'Username': username,
            'Fullname': fullname,
            'Password': password,
            'isAdmin': False,
        })
        print(newUser)
        userSaved = newUser.save()
        return userSaved
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
