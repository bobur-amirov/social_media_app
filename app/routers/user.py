from fastapi import APIRouter, Depends, HTTPException

from app.models import User
from app.schemas import UserCreate, UserOutput
from app.database import get_db
from app.services.utils import hash

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", status_code=201, response_model=UserOutput)
def user_create(user: UserCreate, db: Depends = Depends(get_db)):
    query = db.query(User).filter(User.email == user.email)
    if query.first() is not None:
        raise HTTPException(status_code=409, detail=f"This {user.email} is already registered.")

    user.password = hash(user.password)
    user = User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
