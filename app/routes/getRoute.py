from fastapi import APIRouter
from app.dtos.getRouteDTO import getStationsDTO
from fastapi.responses import JSONResponse
from app.enums.responseEnums import responseENUMS
from app.connectDB import database
import json
from app.querys import all_station_details_query, from_station_details_query, to_station_details_query, from_line_inter_change_station_query, to_line_inter_change_station_query, station_between_same_line_query, stations_with_same_name,get_station_fares_query
from app.models.stationModel import StationModel
from asyncio import gather


router = APIRouter()


fromStation = None
toStation = None


@router.post("/stations")
async def getRouteDetails(request: getStationsDTO):
    if not database.is_connected:
        await database.connect()
    global fromStation
    global toStation

    fromStation = None
    toStation = None
    
    
    

    if (request.fromStation.stationName == request.toStation.stationName):
        return JSONResponse(status_code=401, content={"message": responseENUMS.INVALID_PAYLOAD.value})

    try:
        base_query = f"""{all_station_details_query}"""
        values = {
        }

        fromStationResult, toStationResult = await gather(
            database.fetch_all(
                f"""{base_query},{from_station_details_query} SELECT * FROM fromStationDetail """, values={
                    "fromStationName": f'%{request.fromStation.stationName}%' if request.fromStation.stationName else '',
                    "fromStationNo": '' if not request.fromStation.stationNo else str(request.fromStation.stationNo),
                    "fromStationLineNo": '' if not request.fromStation.lineNo else str(request.fromStation.lineNo),
                }),
            database.fetch_all(
                f"""{base_query},{to_station_details_query} SELECT * FROM toStationDetail """, values={
                    "toStationName": f'%{request.toStation.stationName}%' if request.toStation.stationName else '',
                    "toStationNo": '' if not request.toStation.stationNo else str(request.toStation.stationNo),
                    "toStationLineNo": '' if not request.toStation.lineNo else str(request.toStation.lineNo),

                })
        )
        
        
        
        if (len(fromStationResult) >= 1 and len(toStationResult) >= 1):
            toStation = toStationResult[0]["toStationDetail"]
            toStation = json.loads(toStation)
            for record in fromStationResult:
                if (json.loads(record["fromStationDetail"])["lineNo"] == toStation["lineNo"]):
                    fromStation = json.loads(record["fromStationDetail"])

        if (fromStation is None):
            if (len(fromStationResult) >= 1):
                fromStation = json.loads(
                    fromStationResult[0]["fromStationDetail"])
            else:
                return JSONResponse(status_code=401, content={"message": responseENUMS.INVALID_PAYLOAD.value})

        if (fromStation and toStation):
            if (fromStation["stationName"][0] == toStation["stationName"][0]):
                return JSONResponse(status_code=401, content={"message": responseENUMS.INVALID_PAYLOAD.value})

        if (fromStation and toStation):
            values["fromStationName"] = fromStation["stationName"][0]
            values["fromStationNo"] = str(fromStation["stationNo"])
            values["fromStationLineNo"] = str(fromStation["lineNo"])
            values["toStationName"] = toStation["stationName"][0]
            values["toStationNo"] = str(toStation["stationNo"])
            values["toStationLineNo"] = str(toStation["lineNo"])
        else:
            return JSONResponse(status_code=401, content={"message": responseENUMS.INVALID_PAYLOAD.value})
        

        if (fromStation and toStation):
            fareDetailsResult = await database.fetch_all(get_station_fares_query)
            
            stationFareDetails = None
            fare = None
            try:
                for record in fareDetailsResult:
                    if(fromStation["stationName"][0] == record["stationName"]):
                        stationFareDetails = json.loads(record["fares"])
                index = 0
                for record in fareDetailsResult:
                    if(toStation["stationName"][0] == record["stationName"]):
                        fare = stationFareDetails[index]
                    index+=1 
            except Exception as e:
                print(e)
            

            if (fromStation["lineNo"] == toStation["lineNo"]):
                stationsResult = await database.fetch_all(f"""{base_query},{from_station_details_query},{to_station_details_query},{station_between_same_line_query} SELECT * FROM stationsBetweenSameLine,fromStationDetail,toStationDetail  ORDER BY CASE WHEN ("fromStationDetail"->'stationNo')::int > ("toStationDetail"->'stationNo')::int THEN ("stationDetails"->'stationNo')::int * -1  ELSE  ("stationDetails"->'stationNo')::int END; """, values=values)
                if (stationsResult and len(stationsResult) >= 1):
                    route = []
                    index = 1
                    for record in stationsResult:
                        temp: StationModel = json.loads(
                            record["stationDetails"])
                        temp["stationNo"] = index
                        route.append(temp)
                        index += 1
                        content = {
                            "message": responseENUMS.SUCCESS.value,
                            "fare":fare,
                            "fromStation": fromStation,
                            "toStation": toStation,
                            "route": route
                        }
                    return JSONResponse(
                        status_code=200,
                        content=content
                    )
                else:
                    return JSONResponse(status_code=200, content={"message": responseENUMS.NO_DATA.value})

            else:

                fromInterchageStationsResult, toInterchageStationsResult = await gather(
                    database.fetch_all(
                        f"""{base_query},{from_station_details_query},{from_line_inter_change_station_query} SELECT * FROM fromLineInterChangeStations """, values={
                            "fromStationName": values["fromStationName"],
                            "fromStationNo": values["fromStationNo"],
                            "fromStationLineNo": values["fromStationLineNo"]

                        }),
                    database.fetch_all(
                        f"""{base_query},{to_station_details_query},{to_line_inter_change_station_query} SELECT * FROM toLineInterChangeStations """, values={
                            "toStationName": values["toStationName"],
                            "toStationNo": values["toStationNo"],
                            "toStationLineNo": values["toStationLineNo"]
                        })
                )
                fromInterchangeStations = [json.loads(
                    record["fromLineInterChangeStations"]) for record in fromInterchageStationsResult]
                toInterchangeStations = [json.loads(
                    record["toLineInterChangeStations"]) for record in toInterchageStationsResult]

                if (fromInterchangeStations and toInterchangeStations and len(fromInterchangeStations) >= 1 and len(toInterchangeStations) > 1):

                    tempFromInterchangeStations = []
                    tempToInterChangeStations = []

                    i = 0
                    for record in fromInterchangeStations:
                        j = 0
                        for record2 in toInterchangeStations:
                            if (record["stationName"][0] == record2["stationName"][0]):
                                tempFromInterchangeStations.append(record)
                                tempToInterChangeStations.append(record2)
                                del fromInterchangeStations[i]
                                del toInterchangeStations[j]
                            j += 1
                        i += 1

                    i = 0
                    if (len(fromInterchangeStations) >= 1):
                        for record in fromInterchangeStations:
                            if (toInterchangeStations[i]):
                                
                                temp = await database.fetch_all(f"""{base_query},{stations_with_same_name} SELECT * FROM   stationWithSameName """,values={
                                    "fromStationName":str(
                                    record["stationName"][0]),
                                    "toStationName":str(
                                    toInterchangeStations[i]["stationName"][0]),
                                    "fromLineNo":str(
                                    fromStation["lineNo"]),
                                    "toLineNo":str(toStation["lineNo"])
                                    
                                    
                                })
                                tempFromInterchangeStations.append(
                                    json.loads(temp[0]["stationDetails"]))
                                if (len(temp) > 1):
                                    tempToInterChangeStations.append(
                                        json.loads(temp[1]["stationDetails"]))

                            else:
                                break
                            i += 1

                        i = 0
                        Interchange = []
                        for record in tempFromInterchangeStations:
                            j = 0
                            for record2 in tempToInterChangeStations:
                                if (record["stationName"][0] == record2["stationName"][0]):
                                    Interchange.append({
                                        "fromStation": tempFromInterchangeStations[i],
                                        "toStation": tempToInterChangeStations[j],
                                    })
                                    del tempFromInterchangeStations[i]
                                    del tempToInterChangeStations[j]
                                j += 1

                        if (len(tempToInterChangeStations) >= 1):
                            Interchange.append({
                                "fromStation": tempFromInterchangeStations[0],
                                "toStation": tempToInterChangeStations[0],
                            })

                    fromToInterchange1 = [json.loads(
                        record["stationDetails"]) for record in await database.fetch_all(f"""{base_query} SELECT "stationDetails" FROM stationDetails
                                    WHERE (("stationDetails"->'lineNo' = '{str(fromStation["lineNo"])}' AND  ("stationDetails"->>'stationNo')::int BETWEEN LEAST({fromStation["stationNo"]},{Interchange[0]["fromStation"]["stationNo"]})::int AND GREATEST({fromStation["stationNo"]},{Interchange[0]["fromStation"]["stationNo"]})::int)) """)]

                    toToInterchange1 = [json.loads(
                        record["stationDetails"]) for record in await database.fetch_all(f"""{base_query} SELECT "stationDetails" FROM stationDetails
                                    WHERE (("stationDetails"->'lineNo' = '{str(toStation["lineNo"])}' AND  ("stationDetails"->>'stationNo')::int BETWEEN LEAST({toStation["stationNo"]},{Interchange[0]["toStation"]["stationNo"]})::int AND GREATEST({toStation["stationNo"]},{Interchange[0]["toStation"]["stationNo"]})::int))""")]

                    if (fromStation["stationName"][0] != fromToInterchange1[0]["stationName"][0]):
                        fromToInterchange1 = fromToInterchange1[::-1]

                    if (toStation["stationName"][0] != toToInterchange1[len(toToInterchange1)-1]["stationName"][0]):
                        toToInterchange1 = toToInterchange1[::-1]

                    toToInterchange1 = toToInterchange1[1:len(
                        toToInterchange1)]

                    interChangeRoute2 = []
                    if (len(Interchange) > 1):
                        fromToInterchange2 = [json.loads(
                            record["stationDetails"]) for record in await database.fetch_all(f"""{base_query} SELECT "stationDetails" FROM stationDetails
                                    WHERE (("stationDetails"->'lineNo' = '{str(fromStation["lineNo"])}' AND  ("stationDetails"->>'stationNo')::int BETWEEN LEAST({fromStation["stationNo"]},{fromInterchangeStations[0]["stationNo"]})::int AND GREATEST({fromStation["stationNo"]},{fromInterchangeStations[0]["stationNo"]})::int))""")]

                        interChangeLine2 = [json.loads(
                            record["stationDetails"]) for record in await database.fetch_all(f"""{base_query} SELECT "stationDetails" FROM stationDetails
                                    WHERE (("stationDetails"->'lineNo' = '{str(Interchange[1]["fromStation"]["lineNo"])}' AND  ("stationDetails"->>'stationNo')::int BETWEEN LEAST({Interchange[1]["fromStation"]["stationNo"]},{Interchange[1]["toStation"]["stationNo"]})::int AND GREATEST({Interchange[1]["fromStation"]["stationNo"]},{Interchange[1]["toStation"]["stationNo"]})::int))""")]

                        toInterChange2 = [json.loads(
                            record["stationDetails"]) for record in await database.fetch_all(f"""{base_query} SELECT "stationDetails" FROM stationDetails
                                    WHERE (("stationDetails"->'lineNo' = '{str(toStation["lineNo"])}' AND  ("stationDetails"->>'stationNo')::int BETWEEN LEAST({toStation["stationNo"]},{toInterchangeStations[0]["stationNo"]})::int AND GREATEST({toStation["stationNo"]},{toInterchangeStations[0]["stationNo"]})::int))""")]

                        if (fromStation["stationName"][0] != fromToInterchange2[0]["stationName"][0]):
                            fromToInterchange2 = fromToInterchange2[::-1]

                        if (fromToInterchange2[len(fromToInterchange2)-1]["stationName"][0] != interChangeLine2[0]["stationName"][0]):
                            interChangeLine2 = interChangeLine2[::-1]

                        interChangeLine2 = interChangeLine2[1:len(
                            interChangeLine2)]


                        if (toStation["stationName"][0] != toInterChange2[len(toInterChange2)-1]["stationName"][0]):
                            toInterChange2 = toInterChange2[::-1]
                        toInterChange2 = toInterChange2[1:len(toInterChange2)]
                        

                        interChangeRoute2 = fromToInterchange2+interChangeLine2+toInterChange2

                    interChangeRoute1 = fromToInterchange1+toToInterchange1

                    index = 1
                    for record in interChangeRoute1:
                        interChangeRoute1[index-1]["stationNo"] = index
                        index += 1

                    index = 1
                    for record in interChangeRoute2:
                        interChangeRoute2[index-1]["stationNo"] = index
                        index += 1

                    content = {
                        "message": responseENUMS.SUCCESS.value,
                        "fromStation": fromStation,
                        "toStation": toStation,
                        "fare":fare,

                    }

                    if (len(interChangeRoute1) >= 1 or len(interChangeRoute2) >= 1):
                        if (len(interChangeRoute1) == len(interChangeRoute2)):
                            content["route"] = interChangeRoute1
                            content["route2"] = interChangeRoute2
                        else:
                            if ((len(interChangeRoute1) < len(interChangeRoute2)) or len(interChangeRoute2) == 0):
                                content["route"] = interChangeRoute1
                            else:
                                content["route"] = interChangeRoute2

                    else:
                        return JSONResponse(status_code=200, content={"message": responseENUMS.NO_DATA.value})

                    return JSONResponse(status_code=200, content=content)
                else:
                    return JSONResponse(status_code=200, content={"message": responseENUMS.NO_DATA.value})

        else:
            return JSONResponse(status_code=200, content={"message": responseENUMS.NO_DATA.value})

    except Exception as e:
        raise e
#responseENUMS.INTERNAL_ERROR.value
        return JSONResponse(
            status_code=500,
            content={
                "message":responseENUMS.INTERNAL_ERROR.value
            }
        )
