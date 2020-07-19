import polyjuice
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from professors.models import ProfessorTable


metadata = MetaData()


PotionTable = Table(
    "potions__potion",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column(
        "invented_by",
        Integer,
        ForeignKey(ProfessorTable.c.id),
        django_on_delete="CASCADE",
        django_related_name="invented_potions",
        nullable=False,
    ),
)


@polyjuice.mimic(PotionTable)
class Potion:
    def use(self):
        print(f"*The {self.name} potion is blurping*")
