from fastapi import APIRouter, Depends, HTTPException, status
from app.database.models import User
from app.schemas import UserSchema, Token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import Hasher, create_access_token
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.database.models import get_session
from typing import Annotated
from sqlmodel import Session,select


SessionDep = Annotated[Session, Depends(get_session)]

UserRouter = APIRouter()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

# Utility function to get the current user
def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Query the database for the user
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception

    return user


@UserRouter.post("/register", tags=["User"])
async def register_user(user: UserSchema, session: SessionDep):
    # Check if user already exists
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered.")
    
    # Hash password before storing
    hashed_password = Hasher.get_password_hash(user.password)
    
    # Create new user
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created successfully.", "user": {"first_name": new_user.first_name, "last_name": new_user.last_name, "email": new_user.email}}


# User Login Endpoint
@UserRouter.post("/login", tags=["User"], response_model=Token)  
async def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    # Check if user exists and verify password
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    if not user or not Hasher.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    
    # Create JWT token with expiration time
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}
