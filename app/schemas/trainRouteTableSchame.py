from sqlalchemy import Table, Column, Integer, String, MetaData, JSON
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

trainRouteTable = Table(
    "trainRoutes",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("lineNo", Integer, nullable=False),
    Column("fromStation", JSONB),
    Column("toStation", JSONB),
    Column("noOfStations", Integer),
    Column("stationsDetails", JSONB),
    Column("createdAt", String(50)),
    Column("lastUpdatedAt", String(50)),
)
