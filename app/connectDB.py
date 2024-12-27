from databases import Database


DATABASE_URL = "postgresql://Hyderabadmetroapi_owner:kNfA7vU5nQET@ep-raspy-boat-a5oy6fav.us-east-2.aws.neon.tech/Hyderabadmetroapi?sslmode=require"
database = Database(
    DATABASE_URL)
