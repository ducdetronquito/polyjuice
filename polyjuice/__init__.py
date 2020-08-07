from django.db import models
from .errors import MissingTableDefinition
from .fields import to_django_field
import inspect
from .meta import build_meta_class
from sqlalchemy import Column, Table
from typing import Dict, List


def model(django_model_placeholder):
    model_name = django_model_placeholder.__name__
    module = django_model_placeholder.__module__

    sqlalchemy_table = getattr(django_model_placeholder, "__table__", None)
    if not isinstance(sqlalchemy_table, Table):
        raise MissingTableDefinition(django_model_placeholder)

    user_defined_meta = getattr(django_model_placeholder, "Meta", None)
    Meta = build_meta_class(sqlalchemy_table, user_defined_meta)

    attributes = {
        "__module__": module,
        "__table__": sqlalchemy_table,
        "Meta": Meta,
    }

    _fields = _from_table(sqlalchemy_table)
    attributes.update(_fields)

    methods = _get_methods(django_model_placeholder)
    attributes.update(methods)

    django_model = type(model_name, (models.Model,), attributes)

    return django_model


def _from_table(table: Table) -> Dict[str, models.Field]:
    columns: List[Column] = table.columns.values()
    fields = [to_django_field(table, column) for column in columns]
    return {name: field for name, field in fields}


def _get_methods(django_model):
    methods = inspect.getmembers(django_model, predicate=inspect.isfunction)
    return {method_name: method for method_name, method in methods}
