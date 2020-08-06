from django.db import models
from .errors import PolyjuiceError
from .fields import to_django_field
import inspect
from .meta import build_meta_class
from sqlalchemy import Column, Table
from typing import Dict, List


def mimic(sqlalchemy_table):
    def wrapper(django_model):
        model_name = django_model.__name__

        Meta = build_meta_class(sqlalchemy_table, django_model)

        attributes = {
            "__module__": django_model.__module__,
            "Meta": Meta,
        }

        _fields = _from_table(sqlalchemy_table)
        attributes.update(_fields)

        methods = _get_methods(django_model)
        attributes.update(methods)

        model = type(model_name, (models.Model,), attributes)

        return model

    return wrapper


def _from_table(table: Table) -> Dict[str, models.Field]:
    columns: List[Column] = table.columns.values()
    fields = [to_django_field(table, column) for column in columns]
    return {name: field for name, field in fields}


def _get_methods(django_model):
    methods = inspect.getmembers(django_model, predicate=inspect.isfunction)
    return {method_name: method for method_name, method in methods}
