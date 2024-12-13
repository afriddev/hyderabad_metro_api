

from pydantic import BaseModel


class StationModel(BaseModel):
    stationNo:int
    lineNo:int
    railwaysAndmmts:bool
    busStation:bool
    airportShuttleService:bool    
    terminus:bool
    interChange:bool
    interChangeAndTerminus:bool