from pydantic import BaseModel
from app.models.stationModel import StationModel
from typing import Dict, List



class addTrainRoute(BaseModel):
    lineNo: int
    fromStation: list[str]
    toStation: list[str]
    noOfStations: int
    stationsDetails: list[StationModel]
    key:str

class addFareDTO(BaseModel):
    stationFares: Dict[str, List[int]]
    key:str
    
    