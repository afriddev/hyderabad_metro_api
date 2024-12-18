from pydantic import BaseModel
from typing import Optional


class stationDetailsDTO(BaseModel):
    stationName:str
    lineNo:Optional[int] = None
    stationNo:Optional[int] = None

class getStationsDTO(BaseModel):
    fromStation:stationDetailsDTO
    toStation:stationDetailsDTO
