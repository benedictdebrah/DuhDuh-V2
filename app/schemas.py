from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    title: str = Field(..., description="Title of the post")
    content: str = Field(..., description="Content of the post")

    class Config:
        orm_mode = True    


class UserSchema(BaseModel):
    first_name: str = Field(..., description="First name of the user")  
    last_name: str = Field(..., description="Last name of the user")
    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")

    class Config:
        orm_mode = True

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
