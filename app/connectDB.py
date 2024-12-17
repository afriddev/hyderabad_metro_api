from dotenv import load_dotenv
import os

load_dotenv()


from databases import Database


DATABASE_URL = f"{os.getenv("data_base_url")}"

database = Database(
    DATABASE_URL)
