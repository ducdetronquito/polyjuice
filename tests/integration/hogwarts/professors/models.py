import polyjuice
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from houses.models import HouseTable


metadata = MetaData()


ProfessorTable = Table(
    "professors__professor",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30), nullable=False),
    Column(
        "favourite_house",
        Integer,
        ForeignKey(HouseTable.c.id),
        django_on_delete="CASCADE",
        # The 'django_related_model' option is required when the related model uses a table name
        # that does not match django's pattern <app_name>__<model_name>.
        django_related_model="houses.House",
        nullable=False,
    ),
)


@polyjuice.mimic(ProfessorTable)
class Professor:
    def welcome(self):
        print(f"Welcome to my class, I am Pr. {self.name}.")
