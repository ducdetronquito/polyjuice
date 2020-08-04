from polyjuice import errors
from sqlalchemy import Column, Table
from sqlalchemy.dialects import registry
from sqlalchemy.engine.default import DefaultDialect


# Allows SQLAlchemy column to accept custom attributes specific to the Django ORM.
#
# Example:
# Column('invented_by', Integer, ForeignKey("professors.id"), django_related_name="invented_potions")
#                                                             --------------------------------------
# Will be translated to
# models.ForeignKey(..., related_name="invented_potions")
#                        -------------------------------
class DjangoDialect(DefaultDialect):
    pass


registry.register("django", __name__, "DjangoDialect")


def from_column(table: Table, column: Column):
    options = {
        "null": column.nullable,
    }

    default = column.default
    if default is not None:
        options["default"] = default

    unique = column.unique
    if unique is not None:
        options["unique"] = unique

    django_options = _get_django_specific_options(column)
    if not django_options:
        return options

    if "null" in django_options:
        raise errors.BadNullableFieldSyntax(table, column)

    options.update(django_options)

    return options


def _get_django_specific_options(column):
    return {
        name: value
        for name, value in column.dialect_options["django"].items()
        if name != "*"
    }
