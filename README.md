# Polyjuice ⚗️🧙‍♂️

SQLAlchemy tables disguised as Django models.

[![Build Status](https://api.travis-ci.org/ducdetronquito/polyjuice.svg?branch=master)](https://travis-ci.org/ducdetronquito/polyjuice) [![License](https://img.shields.io/badge/license-public%20domain-ff69b4.svg)](https://github.com/ducdetronquito/polyjuice#license)


## Outline

1. [Usage](https://github.com/ducdetronquito/polyjuice#usage)
2. [Example](https://github.com/ducdetronquito/polyjuice#example)
3. [Work In Progress](https://github.com/ducdetronquito/polyjuice#work-in-progress)
    - [Field options](https://github.com/ducdetronquito/polyjuice#field-options)
    - [Field types](https://github.com/ducdetronquito/polyjuice#field-types)
    - [Meta options](https://github.com/ducdetronquito/polyjuice#meta-options)
4. [Requirements](https://github.com/ducdetronquito/polyjuice#requirements)
5. [License](https://github.com/ducdetronquito/polyjuice#license)


## Usage

*Polyjuice* allows you to define your database tables with [SQLAlchemy Core](https://docs.sqlalchemy.org/en/13/core/) and use them
as legit Django models.

You could find *Polyjuice* relevant in situations where you want manage your table without the Django constraints, but still
take advantage of all the goodness of Django integration and tooling when needed.

I haven't tried every use case yet, but I imagine it could suits many:

- Use other database management tools (ex: migrations with [alembic](https://github.com/sqlalchemy/alembic))
- Take advantage of the async world (ex: build RabbitMQ consummers with database access on top of [aio-pika](https://github.com/mosquito/aio-pika))
- Build complex SQL queries with the SQLAlchemy API and execute them through the Django database connection
- Transition to another web framework
- [Automagically compile your codebase to Rust](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
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


## Work In Progress

### Field options
Cf: [Documentation](https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-options)

- [x] null (via `nullable`) (Q: SQLAlchemy nullable default to True, Django null default to False; what do we choose ?)
- [x] blank (via `django_blank`)
- [ ] choices (via `django_choices`) (Q: Do we also enforce it at the database level ?)
- [x] db_column (via `django_field_name`)
- [ ] db_index
- [ ] db_tablespace
- [x] default
- [x] editable (via `django_editable`)
- [x] error_messages (via `django_error_messages`)
- [x] help_text (via `django_help_text`)
- [ ] primary_key
- [x] unique
- [ ] unique_for_date
- [ ] unique_for_month
- [ ] unique_for_year
- [x] verbose_name (via `django_verbose_name`)
- [x] validators (via `django_validators`)


### Field types
Cf: [Documentation](https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types)

- [x] AutoField
- [x] BigAutoField
- [x] BigIntegerField
- [ ] BinaryField
- [x] BooleanField
- [x] CharField
- [x] DateField (Django options `auto_now` and `auto_now_add` are not enforced at the database level)
- [ ] DateTimeField
- [x] DecimalField
- [ ] DurationField
- [ ] EmailField
- [ ] FileField
- [ ] FilePathField
- [x] FloatField
- [ ] ImageField
- [x] IntegerField
- [ ] GenericIPAddressField
- [x] NullBooleanField
- [ ] PositiveIntegerField
- [ ] PositiveSmallIntegerField
- [ ] SlugField
- [x] SmallIntegerField
- [x] TextField
- [ ] TimeField
- [ ] URLField
- [x] UUIDField

### Meta options
Cf: [Documentation](https://docs.djangoproject.com/en/2.2/ref/models/options/)

- [x] abstract (Forbidden to override)
- [ ] app_label
- [x] base_manager_name
- [x] db_table (Forbidden to override)
- [ ] db_tablespace
- [x] default_manager_name
- [ ] default_related_name
- [x] get_latest_by
- [ ] managed
- [x] order_with_respect_to
- [x] ordering
- [x] permissions
- [x] default_permissions
- [ ] proxy
- [ ] required_db_features
- [ ] required_db_vendor
- [x] select_on_save
- [x] indexes
- [ ] unique_together
- [ ] index_together
- [ ] constraints
- [x] verbose_name
- [x] verbose_name_plural


## Requirements

*Polyjuice* is currently built on top of SQLAlchemy 1.3 and Django 2.2, and requires Python 3.6.


## License

*Polyjuice* is released into the Public Domain. 🎉🍻
