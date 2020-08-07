import polyjuice
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from professors.models import Professor


metadata = MetaData()


@polyjuice.model
class Potion:

    __table__ = Table(
        "potions__potion",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50), nullable=False),
        Column(
            "invented_by",
            Integer,
            ForeignKey(Professor.__table__.c.id),
            django_on_delete="CASCADE",
            django_related_name="invented_potions",
            nullable=False,
        ),
    )

    def use(self):
        print(f"*The {self.name} potion is blurping*")
