from pydantic import BaseModel
from app.models.stationModel import StationModel



class addTrainRoute(BaseModel):
    lineNo: int
    fromStation: list[str]
    toStation: list[str]
    noOfStations: int
    stationsDetails: list[StationModel]

