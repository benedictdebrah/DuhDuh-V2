from app.database.database import engine
from sqlmodel import Field,SQLModel, Relationship,Session
from typing import Optional,List



class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str  
    email: str
    password: str

    # Relationship to Post
    posts: List["Post"] = Relationship(back_populates="user") 


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # Relationship back to User
    user: "User" = Relationship(back_populates="posts")  


# Create all tables in the database
SQLModel.metadata.create_all(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

