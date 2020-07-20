from django.db import models
from polyjuice import errors, fields
import pytest
from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Float, Integer, String

metadata = MetaData()
TestTable = Table("test_table", metadata)


def test_auto_field():
    column = Column("id", Integer, primary_key=True)

    name, django_field = fields.to_django_field(TestTable, column)

    assert isinstance(django_field, models.AutoField)
    assert django_field.auto_created is True
    assert django_field.primary_key is True
    assert django_field.serialize is False
    assert django_field.verbose_name == "ID"
    assert name == "id"


def test_big_auto_field():
    column = Column("id", BigInteger, primary_key=True)

    name, django_field = fields.to_django_field(TestTable, column)

    assert isinstance(django_field, models.BigAutoField)
    assert django_field.auto_created is True
    assert django_field.primary_key is True
    assert django_field.serialize is False
    assert django_field.verbose_name == "ID"
    assert name == "id"


def test_big_integer_field():
    column = Column("distance", BigInteger)

    _, django_field = fields.to_django_field(TestTable, column)

    assert isinstance(django_field, models.BigIntegerField)


def test_boolean_field():
    column = Column("is_a_wizard", Boolean, nullable=False)

    _, django_field = fields.to_django_field(TestTable, column)

    assert isinstance(django_field, models.BooleanField)
    assert django_field.null is False


def test_null_boolean_field():
    column = Column("is_a_wizard", Boolean, nullable=True)

    _, django_field = fields.to_django_field(TestTable, column)

    assert isinstance(django_field, models.NullBooleanField)
    assert django_field.null is True


def test_integer_field():
    column = Column("age", Integer)

    name, django_field = fields.to_django_field(TestTable, column)

    assert isinstance(django_field, models.IntegerField)
    assert name == "age"


def test_float_field():
    column = Column("size", Float)

    _, django_field = fields.to_django_field(TestTable, column)

    assert isinstance(django_field, models.FloatField)


class TestCharField:
    def test_success(self):
        column = Column("name", String(50))

        name, django_field = fields.to_django_field(TestTable, column)

        assert isinstance(django_field, models.CharField)
        assert django_field.max_length == 50
        assert name == "name"

    def test_fail_if_no_length_provided(self):
        column = Column("name", String)

        with pytest.raises(errors.MissingStringLength) as err:
            fields.to_django_field(TestTable, column)

        assert err.value.args[0] == (
            "Table `test_table` column `name`: \n"
            "SQLAlchemy String column must provide a length in order to be converted to a django CharField.\n"
            "Example: Column('name', String(50))"
        )
