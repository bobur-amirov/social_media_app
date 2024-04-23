from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int


class CommentCreate(BaseModel):
    post_id: int
    content: str


class CommentOutput(BaseModel):
    id: int
    content: str
    created: datetime


class PostCreate(BaseModel):
    title: str
    content: str


class PostOutput(PostCreate):
    id: int
    created: datetime
    owner: UserOutput

class PostOutputAll(PostCreate):
    id: int
    created: datetime
    comments: list[CommentOutput]


class LikeSchema(BaseModel):
    post_id: int


class AllFriendSchemaFollower(BaseModel):
    id: int
    follower: UserOutput
    is_following: bool

class AllFriendSchemaFollowing(BaseModel):
    id: int
    following: UserOutput
    is_following: bool

class RoomCreate(BaseModel):
    name: str

class RoomOutput(RoomCreate):
    id: int
    created: datetime