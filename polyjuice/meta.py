from django.db import models
from .errors import InvalidIndexDefinition, PolyjuiceError, UnsupportedFunctionalIndex
from sqlalchemy import Column, Index, Table
from sqlalchemy.sql.expression import UnaryExpression
from typing import List


def build_meta_class(table: Table, user_defined_meta=None):
    class Meta:
        db_table = table.name

    Meta.indexes = get_indexes(table)
    if user_defined_meta is None:
        return Meta

    if hasattr(user_defined_meta, "abstract") and user_defined_meta.abstract:
        raise PolyjuiceError("You cannot mimic an abstract model.")

    if user_defined_meta and hasattr(user_defined_meta, "db_table"):
        raise PolyjuiceError("You cannot override Meta.db_table field.")

    if user_defined_meta and hasattr(user_defined_meta, "indexes"):
        raise PolyjuiceError("You cannot override Meta.indexes field.")

    return Meta


def get_indexes(table: Table) -> List[models.Index]:
    return [convert_index(table, index) for index in table.indexes]


def convert_index(table: Table, index: Index) -> models.Index:
    fields = []
    for expression in index.expressions:
        if isinstance(expression, Column):
            field_name = expression.name
        elif isinstance(expression, UnaryExpression):
            field_name = expression.element.name
            modifier = expression.modifier

            is_descending_index = modifier and modifier.__name__ == "desc_op"

            if is_descending_index:
                field_name = f"-{field_name}"
            else:
                raise InvalidIndexDefinition(table, index)
        else:
            raise UnsupportedFunctionalIndex(table, index)

        fields.append(field_name)

    return models.Index(fields=fields, name=index.name)
