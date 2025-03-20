from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.dtos.configDTO import addTrainRoute, addFareDTO
from app.connectDB import database
from app.enums.responseEnums import responseENUMS
from app.utils.appUtils import get_current_datetime
import json
from app.querys import insert_line_details_query, create_trainroutes_table_routes, create_trainfares_table_routes, insert_fare_details_query
from app.connectDB import SECRET_KEY

router = APIRouter()


@router.post("/addlinedetails")
async def addNewLine(trainRouteDetails: addTrainRoute):
    
    if(trainRouteDetails.key != SECRET_KEY):
        return JSONResponse(
            status_code=401,
                content={
                    "message": responseENUMS.API_KEY_ERROR.value
                }
    
        )
    
  

    
    


    checkTableExistsQuery = "SELECT to_regclass('public.\"trainRoutes\"');"
    checkTableExists = await database.fetch_val(checkTableExistsQuery)

    if checkTableExists is None:

        try:
            await database.execute(create_trainroutes_table_routes)
        except Exception as e:
            print(e)
            return JSONResponse(
                status_code=500,
                content={
                    "message": responseENUMS.INTERNAL_ERROR.value
                }
            )

    try:

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

        await database.execute(insert_line_details_query, values)
        return JSONResponse(
            status_code=200, content={"message": responseENUMS.SUCCESS.value}
        )

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "message": responseENUMS.INTERNAL_ERROR.value
            }
        )


@router.post("/addfaredetails")
async def addFareDetails(request: addFareDTO):
    
    if(request['key'] != SECRET_KEY):
        return JSONResponse(
            status_code=401,
                content={
                    "message": responseENUMS.API_KEY_ERROR.value
                }
    
        )
    checkTableExistsQuery = "SELECT to_regclass('public.\"trainFares\"');"
    checkTableExists = None

    try:
        checkTableExists = await database.fetch_val(checkTableExistsQuery)
        if (checkTableExists == None):
            await database.execute(create_trainfares_table_routes)

        for stationName, fares in request.stationFares.items():
            values = {
                "stationName": stationName,
                "fares": json.dumps(fares),
                "createdAt": get_current_datetime(),
                "lastUpdatedAt": get_current_datetime(),
            }
            await database.execute(insert_fare_details_query, values=values)

        return JSONResponse(
            status_code=200, content={
                "message": responseENUMS.SUCCESS.value
            }
        )

    except Exception as error:
        print(error)
        return JSONResponse(
            status_code=500,
            content={
                "message": responseENUMS.INTERNAL_ERROR.value
            }
        )
