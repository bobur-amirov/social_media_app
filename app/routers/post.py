from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models import Post
from app.schemas import PostCreate, PostOutput, UserOutput, PostOutputAll
from app.services.oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=PostOutput)
def post_create(data: PostCreate, db=Depends(get_db), user: UserOutput=Depends(get_current_user) ):
    print(data, '-----', user)
    new_post = Post(**data.dict(), owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/update/{post_id}', status_code=201, response_model=PostOutput)
def update_my_post(post_id: int, post_data: PostCreate, db: Depends = Depends(get_db),
                   user: UserOutput = Depends(get_current_user)):
    query = db.query(Post).filter(Post.id == post_id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Post doesnt exists!')
    if post.owner_id != user.id:
        raise HTTPException(status_code=400, detail='You don\'t own this post!')
    query.update(post_data.dict(), synchronize_session=False)

    db.commit()
    return post


@router.get('/all', response_model=list[PostOutputAll])
def post_list(db: Session = Depends(get_db)):
    post_list = db.query(Post).all()
    return post_list
