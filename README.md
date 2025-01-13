# DuhDuh-V2

## **Overview**

This project is a web application built with FastAPI that provides a blogging platform with user authentication, post creation, and management. The project is structured to interact with a database (PostgreSQL or SQLite), and includes JWT-based authentication for users. The project is scalable, secure, and designed with modular code for easy maintenance.(for learning purposes)

---

## **Features**

- **User Authentication**:
  - User registration, login, and JWT token-based authentication.
  - Passwords are securely hashed using the `bcrypt` hashing algorithm.
- **Blog Management**:
  - Users can create, update, view, and delete posts.
  - Each post is associated with a user.
- **RESTful API**:
  - The project exposes an API with versioning (`/api/v1`).
  - Endpoints are secured using OAuth2 password-based authentication and JWT tokens.
  
---

## **Technologies Used**

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.10+.
- **SQLModel**: A library for interacting with databases using Pydantic and SQLAlchemy.
- **PostgreSQL** (or SQLite): For storing user and post data.
- **JWT (JSON Web Tokens)**: Used for secure user authentication and authorization.
- **PassLib**: A password hashing library, used for securely storing user passwords.
- **Pydantic**: For settings management and input validation.
- **UV** : python package manager
- **Alembic** : for database migrations

---

## **Project Structure**

```
app/
│
├── core/
│   └── config.py           # Configuration settings (e.g., database URL, JWT secret)
│   └── security.py         # Utility functions for password hashing and token creation
│
├── database/
│   └── models.py           # SQLmodels models (User, Post) and table creation
│   └── database.py         # Database connection setup 
│
├── routers/
│   └── users.py            # User-related routes (registration, login, token handling)
│   └── blog.py             # Blog-related routes (post creation, CRUD operations)
│
├── schemas/
│   └── user.py             # Pydantic models for user input validation
│   └── post.py             # Pydantic models for post input validation
│
├── main.py                 # FastAPI app initialization, routes inclusion
└── .env                    # Environment variables for sensitive configurations (e.g., database URL, JWT secret)
```

---

## **Some little Description**

### **1. Configuration (`core/config.py`)**

The `Settings` class is used to manage all configuration settings in one place. It uses Pydantic's `BaseSettings` to read from environment variables, which allows flexibility in changing configurations between different environments (e.g., development, production).

```python
class Settings(BaseSettings):
    PROJECT_NAME: str = "Try Out DuhDuh"
    PROJECT_VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///database.db"  # SQLite fallback; can be changed to PostgreSQL
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    API_V1_STR: str = "/api/v1"
```

### **2. User Authentication & Security (`core/security.py`)**

#### **JWT Token Generation**

The `create_access_token` function is used to generate a JWT token that expires after a specified time (default or custom). The token is signed using the `SECRET_KEY` and `ALGORITHM` specified in the settings.

```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

#### **Password Hashing**

The `Hasher` class provides methods for hashing passwords and verifying hashed passwords using the `bcrypt` algorithm.

```python
class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
```

### **3. Database Models (`database/models.py`)**

Two SQLModel models are defined:
- **User**: Represents a user with attributes like `first_name`, `last_name`, `email`, and `password`. It has a one-to-many relationship with posts.
- **Post**: Represents a blog post with `title`, `content`, and a foreign key reference to `User`.

```python
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str
    posts: List["Post"] = Relationship(back_populates="user")

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="posts")
```
The database connection is set up using SQLModel. This file also ensures that tables are created in the database.

```python
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```


### **4. Routes (`routers/users.py` and `routers/blog.py`)**

#### **User Routes**

User registration and login are handled in `users.py`. When a user registers, their password is hashed, and a new record is created. On login, the provided password is verified, and a JWT token is returned if the credentials are correct.

```python
@UserRouter.post("/register", tags=["User"])
async def register_user(user: UserSchema, session: SessionDep):
    hashed_password = Hasher.get_password_hash(user.password)
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User created successfully.", "user": new_user.dict()}
```

#### **Blog Routes**

Blog-related routes are handled in `blog.py`. Users can create, read, update, and delete posts. Each post is tied to the user who created it.

```python
@PostRouter.post("/posts")
async def create_post(session: SessionDep, post: PostSchema, current_user: User = Depends(get_current_user)):
    new_post = Post(title=post.title, content=post.content, user_id=current_user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return {"data": new_post.dict()}
```

### **5. Database Connection (`database/database.py`)**

The database connection is set up using SQLModel.

### **6. Main Application (`main.py`)**

The FastAPI application is initialized in `main.py`, where routers for users and posts are included, and the database is initialized on startup.

```python
app = FastAPI(version=settings.API_V1_STR)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
app.include_router(users.UserRouter)
app.include_router(blog.PostRouter)
```

---

## **Running the Application**

### **Prerequisites**
- Python 3.10+
- Install dependencies: `uv install` (having uv installed on your machine - https://docs.astral.sh/uv/#project-management

### **Environment Setup**
1. **Create a `.env` file** with the necessary configurations, such as:
   ```env
   SECRET_KEY="your_secret_key_here"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
   ```

2. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API**:
   - API documentation is available at `/docs` (Swagger UI).
   - Example API paths:
     - `POST /api/v1/user/register`: Register a new user.
     - `POST /api/v1/user/login`: Log in and receive a JWT token.
     - `GET /api/v1/posts`: View all posts.

---

## **Security Considerations**
- **JWT Tokens**:
  - Used for securing API routes. Tokens are validated on every request that requires authentication.
  - Tokens have an expiration time to enhance security.
- **Password Hashing**:
  - Plain-text passwords are never stored in the database. They are hashed using `bcrypt` before storage.

