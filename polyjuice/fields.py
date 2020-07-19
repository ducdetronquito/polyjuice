from django.db.models import (
    AutoField,
    BigAutoField,
    BigIntegerField,
    BooleanField,
    CharField,
    Field,
    ForeignKey,
    IntegerField,
    NullBooleanField,
)
from polyjuice import errors, options, related_fields
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Integer, String
from sqlalchemy import Column, Table
from typing import Tuple, Union


def to_django_field(table: Table, column: Column) -> Tuple[str, Field]:
    _options = options.from_column(table, column)
    column_name = column.name
    column_type = column.type

    if isinstance(column_type, BigInteger):
        field = _to_big_integer_field(table, column, _options)
    elif isinstance(column_type, Boolean):
        field = _to_boolean_field(table, column, _options)
    elif isinstance(column_type, Integer):
        field = _to_integer_field(table, column, _options)
    elif isinstance(column_type, String):
        field = _to_char_field(table, column, _options)
    else:
        raise errors.PolyjuiceError("Case not covered yet")
    return (column_name, field)


def _to_boolean_field(
    table: Table, column: Column, options
) -> Union[BooleanField, NullBooleanField]:
    if options["null"]:
        return NullBooleanField(**options)
    else:
        return BooleanField(**options)


def _to_integer_field(table: Table, column: Column, options) -> IntegerBasedField:
    if column.primary_key:
        return AutoField(
            auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
        )

    if column.foreign_keys:
        return related_fields.to_foreign_key(table, column, options)

    return IntegerField(**options)


BigIntegerBasedField = Union[AutoField, IntegerField]


def _to_big_integer_field(
    table: Table, column: Column, options
) -> BigIntegerBasedField:
    if column.primary_key:
        return BigAutoField(
            auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
        )
    return BigIntegerField(**options)


def _to_char_field(table: Table, column: Column, options) -> CharField:
    max_length = column.type.length
    if max_length is None:
        raise errors.MissingStringLength(table, column)
    return CharField(max_length=column.type.length, **options)
