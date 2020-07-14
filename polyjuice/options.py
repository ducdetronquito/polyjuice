from sqlalchemy.dialects import registry
from sqlalchemy.engine.default import DefaultDialect


__all__ = ["extract"]


# HACK: Allows SQLAlchemy column to accept custom attributes specific to the Django ORM.
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


def from_column(column):
    options = {}
    if column.nullable:
        options["null"] = True

    django_options = _get_django_specific_options(column)
    if django_options:
        options["django"] = django_options

    return options


def _get_django_specific_options(column):
    return {
        name: value
        for name, value in column.dialect_options["django"].items()
        if name != "*"
    }
