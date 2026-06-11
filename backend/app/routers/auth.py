from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from app.core.config import settings
from app.core.database import db
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    decode_token
)
from app.models.user import UserCreate, UserResponse, UserInDB

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInDB(id=str(user["_id"]), **{k: v for k, v in user.items() if k != "_id"})


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    result = await db.users.insert_one(new_user)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return UserResponse(id=str(created_user["_id"]), **{k: v for k, v in created_user.items() if k != "_id" and k != "hashed_password"})


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user["_id"])}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return UserResponse(id=current_user.id, **current_user.model_dump(exclude={"hashed_password"}))


@router.get("/products", tags=["Products"])
async def get_products():
    products = await db.products.find().to_list(length=100)
    return [{"id": str(p["_id"]), **{k: v for k, v in p.items() if k != "_id"}} for p in products]


@router.get("/saved-looks", tags=["Looks"])
async def get_saved_looks():
    looks = await db.saved_looks.find().to_list(length=100)
    return [{"id": str(l["_id"]), **{k: v for k, v in l.items() if k != "_id"}} for l in looks]


@router.get("/fashion-links", tags=["Inspiration"])
async def get_fashion_links():
    links = await db.fashion_links.find().to_list(length=100)
    return [{"id": str(l["_id"]), **{k: v for k, v in l.items() if k != "_id"}} for l in links]


@router.post("/fashion-links", tags=["Inspiration"])
async def add_fashion_link(link_data: dict):
    new_link = await db.fashion_links.insert_one(link_data)
    created_link = await db.fashion_links.find_one({"_id": new_link.inserted_id})
    return {"id": str(created_link["_id"]), **{k: v for k, v in created_link.items() if k != "_id"}}
