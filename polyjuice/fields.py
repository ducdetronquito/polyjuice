from django.db import models
from polyjuice import errors, options, related_fields
from sqlalchemy import Column, Table, types
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import sqltypes
from typing import Tuple, Union


def to_django_field(table: Table, column: Column) -> Tuple[str, models.Field]:
    _options = options.from_column(table, column)

    custom_field_name = _options.pop("field_name", None)
    if custom_field_name:
        column_name = custom_field_name
    else:
        column_name = column.name

    column_type = column.type
    if isinstance(column_type, sqltypes.SmallInteger):
        field = _to_small_integer_field(table, column, _options)
    elif isinstance(column_type, sqltypes.BigInteger):
        field = _to_big_integer_field(table, column, _options)
    elif isinstance(column_type, sqltypes.Boolean):
        field = _to_boolean_field(table, column, _options)
    elif isinstance(column_type, sqltypes.Integer):
        field = _to_integer_field(table, column, _options)
    elif isinstance(column_type, sqltypes.Text):
        field = _to_text_field(table, column, _options)
    elif isinstance(column_type, sqltypes.String):
        field = _to_char_field(table, column, _options)
    elif isinstance(column_type, sqltypes.Float):
        field = _to_float_field(table, column, _options)
    elif isinstance(column_type, postgresql.UUID):
        field = _to_uuid_field(table, column, _options)
    elif isinstance(column_type, sqltypes.Numeric):
        field = _to_decimal_field(table, column, _options)
    else:
        raise errors.PolyjuiceError("Case not covered yet")

    return (column_name, field)


def _to_boolean_field(
    table: Table, column: Column, options
) -> Union[models.BooleanField, models.NullBooleanField]:
    if options["null"]:
        return models.NullBooleanField(**options)
    else:
        return models.BooleanField(**options)


def _to_integer_field(
    table: Table, column: Column, options
) -> Union[models.AutoField, models.IntegerField, models.ForeignKey]:
    if column.primary_key:
        return models.AutoField(
            auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
        )

    if column.foreign_keys:
        return related_fields.to_foreign_key(table, column, options)

    return models.IntegerField(**options)


def _to_big_integer_field(
    table: Table, column: Column, options
) -> Union[models.AutoField, models.IntegerField]:
    if column.primary_key:
        return models.BigAutoField(
            auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
        )
    return models.BigIntegerField(**options)


def _to_char_field(table: Table, column: Column, options) -> models.CharField:
    max_length = column.type.length
    if max_length is None:
        raise errors.MissingStringLength(table, column)
    return models.CharField(max_length=column.type.length, **options)


def _to_float_field(table: Table, column: Column, options) -> models.FloatField:
    return models.FloatField(**options)


def _to_small_integer_field(
    table: Table, column: Column, options
) -> models.SmallIntegerField:
    return models.SmallIntegerField(**options)


def _to_text_field(table: Table, column: Column, options) -> models.TextField:
    return models.TextField(**options)


def _to_uuid_field(table: Table, column: Column, options) -> models.UUIDField:
    if column.type.as_uuid is False:
        raise errors.UuidColumnMissingArgument(table, column)

    return models.UUIDField(**options)


def _to_decimal_field(table: Table, column: Column, options) -> models.DecimalField:
    precision = column.type.precision
    scale = column.type.scale
    if not (isinstance(precision, int) and isinstance(scale, int)):
        raise errors.MissingDecimalFieldArgument(table, column)

    if column.type.asdecimal is False:
        raise errors.InvalidDecimalFieldArgument(table, column)

    return models.DecimalField(max_digits=precision, decimal_places=scale, **options)
