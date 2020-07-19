from django.db import models
from polyjuice import errors
from sqlalchemy import Column, Table


# Cf: https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ForeignKey.on_delete
# TODO: Manage 'SET'
ON_DELETE_MAP = {
    "CASCADE": models.CASCADE,
    "PROTECT": models.PROTECT,
    "SET_NULL": models.SET_NULL,
    "SET_DEFAULT": models.SET_DEFAULT,
    "DO_NOTHING": models.DO_NOTHING,
}


def to_foreign_key(table: Table, column: Column, options) -> models.ForeignKey:
    if "related_model" in options:
        related_model_path = options.pop("related_model")
    else:
        foreign_key = list(column.foreign_keys)[0]
        related_table_name = foreign_key._table_key()
        related_model_path = related_table_name.replace("__", ".")

    if "on_delete" not in options:
        raise errors.MissingOnDeleteOption(table, column)

    on_delete = options["on_delete"]
    try:
        options["on_delete"] = ON_DELETE_MAP[on_delete]
    except KeyError:
        raise errors.InvalidOnDeleteOption(table, column, on_delete)

    return models.ForeignKey(related_model_path, **options)
