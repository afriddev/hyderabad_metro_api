from fastapi import APIRouter
from app.connectDB import database
import json
from fastapi.responses import JSONResponse
from app.dtos.getTrainStationsDTO import getByLineDTO,getByStationNameDTO
from app.enums.responseEnums import responseENUMS

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
        return JSONResponse(
            status_code=400, content={"message":e}
        )


@router.post("/getByLineNo")
async def getDetailsByLine(request: getByLineDTO):
    try:

        if request.stationNo is not None:

            query = """
    SELECT "stationDetails"
    FROM public."trainRoutes", jsonb_array_elements("stationsDetails") AS "stationDetails"
    WHERE "lineNo" = :lineNo 
    AND "stationDetails"->>'stationNo' = :stationNo;
"""

            result = await database.fetch_one(
                query,
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
            status_code=400, content={"message": responseENUMS.INTERNAL_ERROR.value}
        )


@router.post("/getByStationName")
async def getStationDetailsByName(request: getByStationNameDTO):
    try:
        query = """
        SELECT "stationDetails"
        FROM public."trainRoutes",
             jsonb_array_elements("stationsDetails") AS "stationDetails",
             jsonb_array_elements_text("stationDetails"->'stationName') AS "Lang" WHERE LOWER("Lang") ILIKE LOWER(:stationName)
        """

        station_name_with_wildcards = f"%{request.stationName}%"
        values = {"stationName": station_name_with_wildcards}

        if request.stationNo != None:
            query += """ AND ("stationDetails"->>'stationNo' = :stationNo)"""
            values["stationNo"] = str(request.stationNo)

        result = await database.fetch_all(
            query,
            values,
        )
        if result:

            result_dict = []
            for row in result:
                row_dict = dict(row)
                row_dict["stationDetails"] = json.loads(
                    row_dict["stationDetails"])
                result_dict.append(row_dict)

            return JSONResponse(status_code=200, content={"data": result_dict})
        else:
            return JSONResponse(
                status_code=200, content={"data": responseENUMS.NO_DATA.value}
            )

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(
            status_code=400, content={"message": responseENUMS.INTERNAL_ERROR.value}
        )

