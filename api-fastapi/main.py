from fastapi import FastAPI, Request, Response
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
def signUp(user: User):
    try:
        newUser = Users({
            'Username': user.Username,
            'Fullname': user.Fullname,
            'Password': user.Password,
            'isAdmin': user.isAdmin,
        })
        userSaved = newUser.save()
        return userSaved
    except Exception as inst:
        print(inst)
        return {
            'message': str(inst),
            'error': True
        }


@app.post("/sign-in", tags=["users"])
def signIn(user: User):
    try:
        print(user)
        db = HandleDB()
        isValid = db.validateUser(user.Username, user.Password)
        return {
            'isValid': True if isValid["user"] else False,
            'user' : isValid["user"] 
        }
    except Exception as inst:
        print(inst)
        return {
            'message': str(inst),
            'error': True
        }
