from django.db import models
import polyjuice
from polyjuice import errors
import pytest
from sqlalchemy import Column, Integer, MetaData, String, Table
from unittest.mock import Mock, patch


class TestModel:
    def test_success(self):
        class ModelMock:
            pass

        with patch("polyjuice.models") as model_module:
            model_module.Model = ModelMock

            metadata = MetaData()

            @polyjuice.model
            class Professor:

                __table__ = Table(
                    "hogwarts__professor",
                    metadata,
                    Column("id", Integer, primary_key=True),
                    Column("name", String(30), nullable=False),
                )

                def welcome(self):
                    print(f"Welcome to my class, I am Pr. {self.name} 🧙‍♂️")

        assert hasattr(Professor, "__table__")
        assert hasattr(Professor, "welcome")
        # TODO: Assert `Professor` inherits from models.Model

    def test_fail_when_table_definition_is_missing(self):

        with pytest.raises(errors.MissingTableDefinition) as err:

            @polyjuice.model
            class MyModel:
                pass

        assert err.value.args[0] == (
            "Model `MyModel`: \n"
            "A model decorated with `polyjuice.model` must define a `__table__` attribute "
            "which corresponds to its table schema.\n"
            "Cf: https://github.com/ducdetronquito/polyjuice#example"
        )

    def test_fail_when_table_definition_is_invalid(self):

        with pytest.raises(errors.MissingTableDefinition) as err:

            @polyjuice.model
            class MyModel:
                __table__ = "I am not a table"

        assert err.value.args[0] == (
            "Model `MyModel`: \n"
            "A model decorated with `polyjuice.model` must define a `__table__` attribute "
            "which corresponds to its table schema.\n"
            "Cf: https://github.com/ducdetronquito/polyjuice#example"
        )
