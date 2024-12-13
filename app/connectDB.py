from databases import Database

DATABASE_URL = "postgresql://hyderabadmetroapi_user:6wSBPSDAvgOcFbTYDYxIh7dtFWl0PKVa@dpg-cte2jlrtq21c7380enbg-a.oregon-postgres.render.com/hyderabadmetroapi"


database = Database(
    DATABASE_URL)
