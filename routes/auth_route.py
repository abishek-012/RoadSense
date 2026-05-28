from fastapi import APIRouter
from pydantic import BaseModel
from services.firebase_service import db
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserSignup(BaseModel):
    name: str
    email: str
    contact: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# USER SIGNUP
@router.post("/signup")
def signup(user: UserSignup):

    hashed_password = pwd_context.hash(user.password[:72])

    data = {
        "name": user.name,
        "email": user.email,
        "contact": user.contact,
        "password": hashed_password,
        "role": "user",
        "points": 0
    }

    db.collection("users").add(data)

    return {"message": "User registered successfully"}


# LOGIN
@router.post("/login")
def login(data: LoginRequest):

    users = db.collection("users").stream()

    for user in users:

        user_data = user.to_dict()

        if user_data["email"] == data.email:

            if pwd_context.verify(data.password[:72], user_data["password"]):

                return {
                    "status": "success",
                    "role": user_data["role"],
                    "name": user_data["name"]
                }

            else:
                return {"status": "invalid_password"}

    return {"status": "user_not_found"}