# Polyjuice ⚗️🧙‍♂️

SQLAlchemy tables disguised as Django models.

[![Build Status](https://api.travis-ci.org/ducdetronquito/polyjuice.svg?branch=master)](https://travis-ci.org/ducdetronquito/polyjuice) [![License](https://img.shields.io/badge/license-public%20domain-ff69b4.svg)](https://github.com/ducdetronquito/polyjuice#license)


## Usage

*Polyjuice* allows you to define your database tables with [SQLAlchemy Core](https://docs.sqlalchemy.org/en/13/core/) and use them
as legit Django models.

You could find *Polyjuice* relevant in situations where you want manage your table without the Django constraints, but still
take advantage of all the goodness of Django integration and tooling when needed.

I haven't tried every use case yet, but I imagine it could suits many:

- Use other database management tools (ex: migrations with [alembic](https://github.com/sqlalchemy/alembic))
- Take advantage of the async world (ex: build RabbitMQ consummers with [aio-pika](https://github.com/mosquito/aio-pika))
- Build complex SQL queries with the SQLAlchemy API and execute them through the Django database connection
- Transition to another web framework
- ¯\\_(ツ)_/¯


### Example

**In an python package called `my_tables.py`**

```python
"""Here, define your table schemas with the SQLAlchemy core API."""
import polyjuice
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()


ProfessorTable = Table(
    "hogwarts__professor",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30), nullable=False)
)


PotionTable = Table(
    'hogwarts__potion',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column(
        'made_by',
        Integer,
        ForeignKey(ProfessorTable.c.id),
        django_on_delete="CASCADE",
        django_related_name="personal_potions"
    )
)
```

**In your Django project**

```python
from my_tables import PotionTable, ProfessorTable
import polyjuice


@polyjuice.mimic(ProfessorTable)
class Professor:
    """The Polyjuice decorator will turn this class into a legit Django model."""

    def welcome(self):
        print(f"Welcome to my class, I am Pr. {self.name} 🧙‍♂️")


@polyjuice.mimic(PotionTable)
class Potion:
    """This class too"""

    def boil(self):
        print(f"*The {self.name} potion is blurping* ⚗️")


# And you are ready to go !
severus_snape = Professor.objects.create(name="Severus Snape")
veritaserum = Professor.objects.create(name="Veritaserum", made_by=severus_snape)

assert severus_snape.personal_potions.count() == 1
```


## Requirements

*Polyjuice* is currently built on top of SQLAlchemy 1.3 and Django 2.2, and requires Python 3.6.


## License

*Polyjuice* is released into the Public Domain. 🎉🍻
