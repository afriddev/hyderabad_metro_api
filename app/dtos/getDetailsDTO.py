from pydantic import BaseModel
from typing import Optional


class getByLineDTO(BaseModel):
    lineNo: int
    stationNo: Optional[int] = None

class getByStationNameDTO(BaseModel):
    stationName:str
    stationNo:Optional[int] = None

