from databases import Database


DATABASE_URL = "postgresql://neondb_owner:7Eazfni3Uomg@ep-winter-sound-a5vrl30y.us-east-2.aws.neon.tech/neondb?sslmode=require"
database = Database(
    DATABASE_URL)
