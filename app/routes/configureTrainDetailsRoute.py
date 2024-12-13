from fastapi import APIRouter
from app.dtos.addTrainDTO import addTrainDTO
from app.connectDB import database

router = APIRouter()

@router.post("/addtrainroutedetails")
async def addTrainRoute(trainRoute: addTrainDTO):
    # Step 1: Check if the table exists in the correct schema
    check_table_query = "SELECT to_regclass('public.trainRoutes')"
    
    try:
        table_exists = await database.fetch_val(check_table_query)
        
        if table_exists is None:
            # Table does not exist, so create it
            create_table_query = """
                CREATE TABLE public.trainRoutes (
                    id SERIAL PRIMARY KEY,
                    lineNo INTEGER NOT NULL,
                    fromStation VARCHAR(50),
                    toStation VARCHAR(50),
                    noOfStations INTEGER,
                    stationsDetails JSON,
                    createdAt VARCHAR(50),
                    lastUpdatedAt VARCHAR(50)
                );
            """
            await database.execute(create_table_query)
            print("Table created successfully")
        
        # Step 2: Proceed with inserting data into the table
        insert_query = """
            INSERT INTO public.trainRoutes (lineNo, fromStation, toStation, noOfStations, stationsDetails, createdAt, lastUpdatedAt)
            VALUES (:lineNo, :fromStation, :toStation, :noOfStations, :stationsDetails, :createdAt, :lastUpdatedAt);
        """
        await database.execute(insert_query, values={
            "lineNo": trainRoute.lineNo,
            "fromStation": trainRoute.fromStation,
            "toStation": trainRoute.toStation,
            "noOfStations": trainRoute.noOfStations,
            "stationsDetails": {},
            "createdAt": "2024-12-13",
            "lastUpdatedAt": "2024-12-13"
        })
        return {"message": "Train route added successfully"}

    except Exception as e:
        print(e)
        return {"message": "An error occurred while adding the route"}
