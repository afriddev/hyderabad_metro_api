from fastapi import APIRouter
from app.connectDB import database
import json
from fastapi.responses import JSONResponse
from app.dtos.getDetailsDTO import getByLineDTO, getByStationNameDTO
from app.enums.responseEnums import responseENUMS
from app.querys import all_station_details_query, get_stations_in_line_query

router = APIRouter()


@router.get("/all")
async def getAllTrainRouteDetails():
    try:
        selectQuery = 'SELECT * FROM public."trainRoutes";'
        result = await database.fetch_all(selectQuery)
        parsed_result = []
        for record in result:
            record_dict = dict(record)
            record_dict["fromStation"] = json.loads(record_dict["fromStation"])
            record_dict["toStation"] = json.loads(record_dict["toStation"])
            record_dict["stationsDetails"] = json.loads(
                record_dict["stationsDetails"])
            parsed_result.append(record_dict)

        return JSONResponse(
            status_code=200,
            content={"message": responseENUMS.SUCCESS.value,
                     "data": parsed_result},
        )
    except Exception as e:
        print(e)
        
        print("hello")

        return JSONResponse(
            status_code=200, content={"message": e}
        )


@router.post("/getbylineno")
async def getDetailsByLine(request: getByLineDTO):
    try:

        if request.stationNo is not None:

            result = await database.fetch_one(
                get_stations_in_line_query,
                values={"lineNo": request.lineNo,
                        "stationNo": str(request.stationNo)},
            )
            parsed_result = dict(result)
            parsed_result["stationDetails"] = json.loads(
                parsed_result["stationDetails"]
            )

            if result:
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": responseENUMS.SUCCESS.value,
                        "data": parsed_result,
                    },
                )

            else:
                return JSONResponse(
                    status_code=200, content={"message": responseENUMS.NO_DATA.value}
                )

        else:

            query = 'SELECT * FROM public."trainRoutes" WHERE "lineNo" = :lineNo ;'
            result = await database.fetch_one(query, values={"lineNo": request.lineNo})
            if result:
                parsed_result = dict(result)

                parsed_result["fromStation"] = json.loads(
                    parsed_result["fromStation"])
                parsed_result["toStation"] = json.loads(
                    parsed_result["toStation"])
                parsed_result["stationsDetails"] = json.loads(
                    parsed_result["stationsDetails"]
                )

                return JSONResponse(
                    status_code=200,
                    content={
                        "message": responseENUMS.SUCCESS.value,
                        "data": parsed_result,
                    },
                )

            else:
                return JSONResponse(
                    status_code=200, content={"message": responseENUMS.NO_DATA.value}
                )

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": responseENUMS.INTERNAL_ERROR.value
            }
        )


@router.get("/allstations")
async def getAllStations():

    try:
        allStationResult = await database.fetch_all(f"""{all_station_details_query} SELECT "stationDetails"  FROM stationDetails """)

        parsed_result = []
        for record in allStationResult:
            parsed_result.append(json.loads(record["stationDetails"]))

        unique_stations = {}
        for station in parsed_result:
            key = station["stationName"][0]
            if key not in unique_stations:
                station.pop("createdAt", None)
                station.pop("lastUpdatedAt", None)
                unique_stations[key] = station

        unique_stations_list = list(unique_stations.values())

        return JSONResponse(
            status_code=200,
            content={
                "message": responseENUMS.SUCCESS.value,
                "data": unique_stations_list
            }
        )

    except Exception as e:
        print(e)
        # responseENUMS.INTERNAL_ERROR.value
        return JSONResponse(
            status_code=500,
            content={
                "message":e
            }
        )
