from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = "postgresql://Hyderabadmetroapi_owner:kNfA7vU5nQET@ep-raspy-boat-a5oy6fav.us-east-2.aws.neon.tech/Hyderabadmetroapi?sslmode=require"
SECRET_KEY  = "ALIEN"

database = Database(
    DATABASE_URL)