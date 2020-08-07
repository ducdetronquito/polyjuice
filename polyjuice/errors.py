from sqlalchemy import Column, Index, Table


class PolyjuiceError(Exception):
    pass


class MissingOnDeleteOption(PolyjuiceError):
    def __init__(self, table: Table, column: Column) -> None:
        message = (
            f"Table `{table.name}` column `{column.name}`: \n"
            "SQlAlchemy ForeignKey column must provide a 'django_on_delete' value "
            "as it is mandatory for a Django ForeignKey field.\n"
            "Example: Column('invented_by', Integer, ForeignKey('myrelatedmodel.id'), django_on_delete='CASCADE')"
        )
        super().__init__(message)


class InvalidOnDeleteOption(PolyjuiceError):
    def __init__(self, table: Table, column: Column, on_delete: str) -> None:
        message = (
            f"Table `{table.name}` column `{column.name}`: \n"
            f"The value `{on_delete}` is not valid for the 'django_on_delete' option.\n"
            "You must use either: CASCADE, PROTECT, SET_NULL, SET_DEFAULT or DO_NOTHING.\n"
            "Cf: https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ForeignKey.on_delete"
        )
        super().__init__(message)


class MissingStringLength(PolyjuiceError):
    def __init__(self, table: Table, column: Column) -> None:
        message = (
            f"Table `{table.name}` column `{column.name}`: \n"
            "SQLAlchemy String column must provide a length in order to be converted to a django CharField.\n"
            "Example: Column('name', String(50))"
        )
        super().__init__(message)


class BadNullableFieldSyntax(PolyjuiceError):
    def __init__(self, table: Table, column: Column) -> None:
        message = (
            f"Table `{table.name}` column `{column.name}`: \n"
            "To define a NULLABLE SQLAlchemy column, use the argument `nullable` instead of the `django_null` option.\n"
            "Example: Column('name', String(50), nullable=True)"
        )
        super().__init__(message)


class UuidColumnMissingArgument(PolyjuiceError):
    def __init__(self, table: Table, column: Column) -> None:
        message = (
            f"Table `{table.name}` column `{column.name}`: \n"
            "To define a UUID column, you must enable the conversion to python uuid objects.\n"
            "Example: Column('my_uuid', UUID(as_uuid=True))\n"
            "Cf: https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.UUID"
        )
        super().__init__(message)


class InvalidDecimalFieldArgument(PolyjuiceError):
    def __init__(self, table: Table, column: Column) -> None:
        message = (
            f"Table `{table.name}` column `{column.name}`: \n"
            "To define a Decimal column, the argument `asdecimal` must be kept unset or set to `True` "
            "to ensure that values are returned as python Decimal objects.\n"
            "Example: Column('fees', Numeric(precision=10, scale=5))\n"
        )
        super().__init__(message)


class MissingDecimalFieldArgument(PolyjuiceError):
    def __init__(self, table: Table, column: Column) -> None:
        message = (
            f"Table `{table.name}` column `{column.name}`: \n"
            "To define a Decimal column, the argument `precision` and `scale` must be set.\n"
            "Example: Column('fees', Numeric(precision=10, scale=5))\n"
        )
        super().__init__(message)


class InvalidIndexDefinition(PolyjuiceError):
    def __init__(self, table: Table, index: Index) -> None:
        message = (
            f"Table `{table.name}` index `{index.name}`: \n"
            "Invalid index definition.\n"
            "Example: Index('some_index', some_table.c.some_column)\n"
            "Cf: https://docs.sqlalchemy.org/en/13/core/constraints.html#indexes"
        )
        super().__init__(message)


class UnsupportedFunctionalIndex(PolyjuiceError):
    def __init__(self, table: Table, index: Index) -> None:
        message = (
            f"Table `{table.name}` index `{index.name}`: \n"
            "Only descending index is supported yet.\n"
            "Example: Index('some_index', some_table.c.some_column.desc())\n"
            "Cf: https://docs.sqlalchemy.org/en/13/core/constraints.html#functional-indexes"
        )
        super().__init__(message)


class MissingTableDefinition(PolyjuiceError):
    def __init__(self, django_model_placeholder) -> None:
        message = (
            f"Model `{django_model_placeholder.__name__}`: \n"
            "A model decorated with `polyjuice.model` must define a `__table__` attribute "
            "which corresponds to its table schema.\n"
            "Cf: https://github.com/ducdetronquito/polyjuice#example"
        )
        super().__init__(message)
