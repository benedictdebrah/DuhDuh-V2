from sqlmodel import create_engine
from dotenv import load_dotenv
from app.core.config import settings



load_dotenv()

database_url = settings.DATABASE_URL

engine = create_engine(database_url, echo=True)


