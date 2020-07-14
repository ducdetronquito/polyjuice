import polyjuice
from sqlalchemy import Table, Column, Integer, String, MetaData


metadata = MetaData()


HouseTable = Table(
    "hogwarts_houses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
)


@polyjuice.mimic(HouseTable)
class House:
    pass
