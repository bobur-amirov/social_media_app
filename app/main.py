from fastapi import FastAPI

from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.post import router as post_router
from app.routers.comment import router as comment_router
from app.routers.follower import router as follower_router
from app.routers.chat import router as chat_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(follower_router)
app.include_router(chat_router)

