from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY  = os.getenv("SECRET_KEY")

database = Database(
    DATABASE_URL)