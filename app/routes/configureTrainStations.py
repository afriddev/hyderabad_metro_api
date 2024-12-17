from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.dtos.configTrainRoutesDTO import addTrainRoute
from app.connectDB import database
from app.enums.responseEnums import responseENUMS
from app.utils.appUtils import get_current_datetime
import json

router = APIRouter()


@router.post("/addtrainroutedetails")
async def addTrainRouteDetails(trainRouteDetails: addTrainRoute):    
    checkTableExistsQuery = "SELECT to_regclass('public.\"trainRoutes\"');"
    checkTableExists = await database.fetch_val(checkTableExistsQuery)

    if checkTableExists is None:
        createTableQuery = """
        CREATE TABLE public.\"trainRoutes\"(
            id SERIAL PRIMARY KEY,
            "lineNo" INTEGER NOT NULL,
            "fromStation" JSONB,
            "toStation" JSONB,
            "noOfStations" INTEGER,
            "stationsDetails" JSONB,
            "createdAt" VARCHAR(200),
            "lastUpdatedAt" VARCHAR(200)
        );
        """
        try:
            await database.execute(createTableQuery)
        except Exception as e:
            print(e)
            return JSONResponse(
                status_code=400, content={"message": responseENUMS.INTERNAL_ERROR.value}
            )

    try:
        insertQuery = """
                INSERT INTO public.\"trainRoutes\" ("lineNo", "fromStation", "toStation", "noOfStations", "stationsDetails", "createdAt", "lastUpdatedAt")
                VALUES(:lineNo, :fromStation, :toStation, :noOfStations, :stationsDetails, :createdAt, :lastUpdatedAt);
        """
        values = {
            "lineNo": trainRouteDetails.lineNo,
            "fromStation": json.dumps(trainRouteDetails.fromStation),
            "toStation": json.dumps(trainRouteDetails.toStation),
            "noOfStations": trainRouteDetails.noOfStations,
            "stationsDetails": json.dumps(
                [station.dict() for station in trainRouteDetails.stationsDetails]
            ),
            "createdAt": get_current_datetime(),
            "lastUpdatedAt": get_current_datetime(),
        }

        await database.execute(insertQuery, values)
        return JSONResponse(
            status_code=200, content={"message": responseENUMS.SUCCESS.value}
        )

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=400, content={"message": responseENUMS.INTERNAL_ERROR.value}
        )
