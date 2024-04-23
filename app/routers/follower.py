from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette import status

from app.database import get_db
from app.schemas import AllFriendSchemaFollower, AllFriendSchemaFollowing
from app.services.oauth2 import get_current_user
from app.models import User, Followers

router = APIRouter(prefix="/follower", tags=["follower"])


@router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
def add_follower(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id == current_user.id:
        raise HTTPException(status_code=403, detail="You can't follow yourself")
    follower = Followers(following_id=current_user.id, follower_id=user.id)
    db.add(follower)
    db.commit()
    db.refresh(follower)
    return {"message": "Follower added"}


@router.post("/is-following/{user_id}", status_code=status.HTTP_201_CREATED)
def is_following(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    follower = db.query(Followers).filter(Followers.following_id == user.id, Followers.follower_id == current_user.id)
    if not follower.first():
        raise HTTPException(status_code=403, detail="You can't follow user")
    follower.update({"is_following": True})
    db.commit()
    return {"message": "User followed"}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_follower(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    follower = db.query(Followers).filter(Followers.following_id == user.id, Followers.follower_id == current_user.id)
    if not follower.first():
        raise HTTPException(status_code=403, detail="You can't follow user")
    follower.delete()
    db.commit()
    return {"message": "User deleted"}


@router.get("/all-followers", status_code=status.HTTP_200_OK, response_model=list[AllFriendSchemaFollower])
def get_followers(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    follower = db.query(Followers).filter(Followers.following_id == current_user.id)
    return follower


@router.get("/all-following", status_code=status.HTTP_200_OK, response_model=list[AllFriendSchemaFollowing])
def get_following(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    following = db.query(Followers).filter(Followers.follower_id == current_user.id)
    return following