from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.schemas import CommentCreate, CommentOutput
from app.database import get_db
from app.services.oauth2 import get_current_user
from app.models import Post, Comment

router = APIRouter(prefix="/comment", tags=["comments"])


@router.post("/", response_model=CommentOutput, status_code=201)
async def create_comment(comment: CommentCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        return HTTPException(status_code=404, detail="Post not found")
    new_comment = Comment(post_id=post.id, owner_id=user.id, content=comment.content)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
