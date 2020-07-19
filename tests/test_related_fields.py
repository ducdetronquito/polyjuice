from django.db import models
from polyjuice import errors, fields
import pytest
from sqlalchemy import Column, ForeignKey, MetaData, Table
from sqlalchemy.sql.sqltypes import Integer

metadata = MetaData()
TestTable = Table("test_table", metadata)


class TestForeignKey:
    def test_success(self):
        column = Column(
            "invented_by", Integer, ForeignKey("mymodel.id"), django_on_delete="CASCADE"
        )

        name, django_field = fields.to_django_field(TestTable, column)

        assert isinstance(django_field, models.ForeignKey)
        assert django_field.remote_field.model == "mymodel"
        assert django_field.remote_field.on_delete == models.CASCADE
        assert name == "invented_by"

    def test_related_model_is_prefixed_by_the_django_app_name(self):
        column = Column(
            "invented_by",
            Integer,
            ForeignKey("myshinyapp__mymodel.id"),
            django_on_delete="CASCADE",
        )

        _, django_field = fields.to_django_field(TestTable, column)

        assert django_field.remote_field.model == "myshinyapp.mymodel"

    def test_django_related_name_option(self):
        column = Column(
            "invented_by",
            Integer,
            ForeignKey("myshinyapp__mymodel.id"),
            django_on_delete="CASCADE",
            django_related_name="mymodels",
        )

        _, django_field = fields.to_django_field(TestTable, column)
        assert django_field.remote_field.related_name == "mymodels"

    def test_fail_if_no_on_delete_is_provided(self):
        column = Column("invented_by", Integer, ForeignKey("mymodel.id"))

        with pytest.raises(errors.MissingOnDeleteOption) as err:
            fields.to_django_field(TestTable, column)

        assert err.value.args[0] == (
            "Table `test_table` column `invented_by`: \n"
            "SQlAlchemy ForeignKey column must provide a 'django_on_delete' value "
            "as it is mandatory for a Django ForeignKey field.\n"
            "Example: Column('invented_by', Integer, ForeignKey('myrelatedmodel.id'), django_on_delete='CASCADE')"
        )

    def test_fail_if_on_delete_option_is_not_valid(self):
        column = Column(
            "invented_by", Integer, ForeignKey("mymodel.id"), django_on_delete="lmfao"
        )

        with pytest.raises(errors.InvalidOnDeleteOption) as err:
            fields.to_django_field(TestTable, column)

        assert err.value.args[0] == (
            "Table `test_table` column `invented_by`: \n"
            "The value `lmfao` is not valid for the 'django_on_delete' option.\n"
            "You must use either: CASCADE, PROTECT, SET_NULL, SET_DEFAULT or DO_NOTHING.\n"
            "Cf: https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ForeignKey.on_delete"
        )
