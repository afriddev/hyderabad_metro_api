

from pydantic import BaseModel


class StationModel(BaseModel):
    stationNo:int
    lineNo:int
    railwaysAndMMTS:bool
    busStation:bool
    airportShuttleService:bool    
    terminus:bool
    interChange:bool
    interChangeAndTerminus:bool
    stationName:list[str]