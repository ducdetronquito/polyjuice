from polyjuice import errors, fields
import pytest
from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Integer


metadata = MetaData()
TestTable = Table("test_table", metadata)


def test_blank():
    column = Column("age", Integer, django_blank=True)

    _, django_field = fields.to_django_field(TestTable, column)

    assert django_field.blank is True


def test_editable():
    column = Column("age", Integer, django_editable=False)

    _, django_field = fields.to_django_field(TestTable, column)

    assert django_field.editable is False


def test_error_messages():
    error_messages = {"__all__": "It's leviosa, not leviosaaaa!"}
    column = Column("age", Integer, django_error_messages=error_messages)

    _, django_field = fields.to_django_field(TestTable, column)

    assert django_field.error_messages["__all__"] == "It's leviosa, not leviosaaaa!"


def test_help_text():
    column = Column(
        "age", Integer, django_help_text="Number of years since your birth day"
    )

    _, django_field = fields.to_django_field(TestTable, column)

    assert django_field.help_text == "Number of years since your birth day"


def test_verbose_name():
    column = Column(
        "ag",
        Integer,
        django_verbose_name="This column was supposed to be named 'age', but my 'E' key was broke at the time.",
    )

    _, django_field = fields.to_django_field(TestTable, column)

    assert (
        django_field.verbose_name
        == "This column was supposed to be named 'age', but my 'E' key was broke at the time."
    )


def test_validator():
    def validate_is_old_enough(value):
        from django.core.exceptions import ValidationError

        if value < 11:
            raise ValidationError("Don't try to fool Hagrid kid...")

    column = Column("age", Integer, django_validators=[validate_is_old_enough])

    _, django_field = fields.to_django_field(TestTable, column)

    try:
        # HACK: Don't judge me.
        django_field.validators[0]
    except:
        pass

    assert django_field.validators[0] == validate_is_old_enough


class TestDbColumn:
    def test_success(self):
        column = Column("age", Integer, django_field_name="my_age")

        name, _ = fields.to_django_field(TestTable, column)

        assert name == "my_age"

    def test_fail_when_field_name_is_empty(self):
        column = Column("age", Integer, django_field_name="")

        name, _ = fields.to_django_field(TestTable, column)

        assert name == "age"


class TestNull:
    def test_null(self):
        column = Column("age", Integer, nullable=True)

        _, django_field = fields.to_django_field(TestTable, column)

        assert django_field.null is True

    def test_not_null(self):
        column = Column("age", Integer, nullable=False)

        _, django_field = fields.to_django_field(TestTable, column)

        assert django_field.null is False

    def test_fail_when_using_django_options(self):
        column = Column("age", Integer, django_null=False)

        with pytest.raises(errors.BadNullableFieldSyntax) as err:
            fields.to_django_field(TestTable, column)

        assert err.value.args[0] == (
            "Table `test_table` column `age`: \n"
            "To define a NULLABLE SQLAlchemy column, use the argument `nullable` instead of the `django_null` option.\n"
            "Example: Column('name', String(50), nullable=True)"
        )
