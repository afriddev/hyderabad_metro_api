from databases import Database


DATABASE_URL = "postgres://neondb_owner:7Eazfni3Uomg@ep-winter-sound-a5vrl30y-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
database = Database(
    DATABASE_URL)
