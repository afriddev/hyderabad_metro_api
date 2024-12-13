from sqlalchemy import Table, Column, Integer, String, MetaData, JSON

metadata = MetaData()
trainRouteTable = Table(
    "trainRoutes",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("lineNo", Integer),
    Column("fromStation", String(50)),
    Column("toStation", String(50)),
    Column("noOfStations", Integer),
    Column("stationsDetails", JSON),
    Column("createdAt", String(50)),
    Column("lastUpdatedAt", String(50)),
)
