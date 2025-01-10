from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database.models import Post, User
from app.schemas import PostSchema
from app.routers.users import get_current_user
from app.database.models import get_session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

SessionDep = Annotated[Session, Depends(get_session)]

PostRouter = APIRouter(tags=["Posts"])

# Routes

# Create a Post
@PostRouter.post("/posts")
async def create_post(
    session: SessionDep, post: PostSchema, current_user: User = Depends(get_current_user)
) -> dict:
    new_post = Post(title=post.title, content=post.content, user_id=current_user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return {"data": new_post.dict()}

# Get all Posts
@PostRouter.get("/posts")
async def get_posts(session: SessionDep) -> dict:
    statement = select(Post)
    posts = session.exec(statement).all()
    return {"data": [post.dict() for post in posts]}

# Get a single Post
@PostRouter.get("/posts/{id}")
async def get_single_post(id: int, session: SessionDep) -> dict:
    statement = select(Post).where(Post.id == id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(status_code=404, detail="No such post with the supplied ID.")
    return {"data": post.dict()}

# Update a Post
@PostRouter.put("/posts/{id}")
async def update_post(
    session: SessionDep, id: int, post: PostSchema, current_user: User = Depends(get_current_user)
) -> dict:
    statement = select(Post).where(Post.id == id, Post.user_id == current_user.id)
    post_to_update = session.exec(statement).first()
    if not post_to_update:
        raise HTTPException(status_code=404, detail="No such post with the supplied ID.")
    
    # Update the post fields
    for key, value in post.dict().items():
        setattr(post_to_update, key, value)
    
    session.commit()
    session.refresh(post_to_update)
    return {"data": post_to_update.dict()}

# Delete a Post
@PostRouter.delete("/posts/{id}")
async def delete_post(
    session: SessionDep, id: int, current_user: User = Depends(get_current_user)
) -> dict:
    statement = select(Post).where(Post.id == id, Post.user_id == current_user.id)
    post_to_delete = session.exec(statement).first()
    if not post_to_delete:
        raise HTTPException(status_code=404, detail="No such post with the supplied ID.")
    
    session.delete(post_to_delete)
    session.commit()
    return {"data": "Post deleted successfully."}
