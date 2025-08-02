from fastapi import APIRouter, HTTPException, status, Depends
from backend.models import UserCreate, UserLogin, Token
from backend.auth import hash_password, verify_password, create_access_token
from backend.db import user_collection
from bson.objectid import ObjectId
from datetime import timedelta
from pymongo.errors import DuplicateKeyError

auth_router = APIRouter()

user_collection.create_index("email", unique=True)


@auth_router.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)

    try:
        result = await user_collection.insert_one(user_dict)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/login", response_model=Token)
async def login(user: UserLogin):
    stored_user = await user_collection.find_one({"email": user.email})
    if not stored_user or not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email, "role": stored_user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}
