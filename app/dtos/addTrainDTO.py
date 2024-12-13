from pydantic import BaseModel
from app.models.stationModel import StationModel


class addTrainDTO(BaseModel):
    lineNo: int
    fromStation: str
    toStation: str
    noOfStations: int
    stationsDetails: list[StationModel]
