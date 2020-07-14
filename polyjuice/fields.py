from django.db.models import AutoField, CharField, Field, ForeignKey, IntegerField
from polyjuice import errors, options, related_fields
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Column, Table
from typing import Tuple, Union


def to_django_field(table: Table, column: Column) -> Tuple[str, Field]:
    _options = options.from_column(column)
    column_name = column.name
    column_type = column.type
    if isinstance(column_type, Integer):
        field = _to_integer_field(table, column, _options)
    elif isinstance(column_type, String):
        field = _to_char_field(table, column, _options)
    else:
        raise PolyjuiceError("Case not covered yet")
    return (column_name, field)


IntegerBasedField = Union[AutoField, IntegerField, ForeignKey]


def _to_integer_field(table: Table, column: Column, options) -> IntegerBasedField:
    if column.primary_key:
        return AutoField(
            auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
        )

    if column.foreign_keys:
        return related_fields.to_foreign_key(table, column, options)

    return IntegerField(**options)


def _to_char_field(table: Table, column: Column, options) -> CharField:
    max_length = column.type.length
    if max_length is None:
        raise errors.MissingStringLength(table, column)
    return CharField(max_length=column.type.length, **options)
