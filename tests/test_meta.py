from django.db import models
from polyjuice import errors, meta
import pytest
from sqlalchemy import Column, func, Index, Integer, MetaData, String, Table


class TestConvertIndex:
    def setup(self):
        metadata = MetaData()
        self.table = Table(
            "test_table", metadata, Column("name", String(50)), Column("age", Integer),
        )

    def test_single_field(self):
        index = Index("my_super_index", self.table.c.name)

        django_index = meta.convert_index(self.table, index)

        assert django_index.name == "my_super_index"
        assert django_index.fields == ["name"]

    def test_multiple_field(self):
        index = Index("my_super_index", self.table.c.name, self.table.c.age)

        django_index = meta.convert_index(self.table, index)

        assert django_index.name == "my_super_index"
        assert django_index.fields == ["name", "age"]

    def test_descending_index(self):
        index = Index("my_super_index", self.table.c.name.desc())

        django_index = meta.convert_index(self.table, index)

        assert django_index.name == "my_super_index"
        assert django_index.fields == ["-name"]

    def test_fail_when_using_unsupported_functional_index(self):
        index = Index("my_super_index", func.lower(self.table.c.name))

        with pytest.raises(errors.UnsupportedFunctionalIndex) as err:
            meta.convert_index(self.table, index)

        assert err.value.args[0] == (
            "Table `test_table` index `my_super_index`: \n"
            "Only descending index is supported yet.\n"
            "Example: Index('some_index', some_table.c.some_column.desc())\n"
            "Cf: https://docs.sqlalchemy.org/en/13/core/constraints.html#functional-indexes"
        )

    def test_fail_when_defining_invalid_index(self):
        index = Index("my_super_index", self.table.c.name.distinct())

        with pytest.raises(errors.InvalidIndexDefinition) as err:
            meta.convert_index(self.table, index)

        assert err.value.args[0] == (
            "Table `test_table` index `my_super_index`: \n"
            "Invalid index definition.\n"
            "Example: Index('some_index', some_table.c.some_column)\n"
            "Cf: https://docs.sqlalchemy.org/en/13/core/constraints.html#indexes"
        )


class TestBuildMetaClass:
    def setup(self):
        metadata = MetaData()
        self.table = Table("test_table", metadata, Column("name", String(50)),)

        class Meta:
            pass

        self.user_defined_meta = Meta

    def test_db_table(self):
        Meta = meta.build_meta_class(self.table, self.user_defined_meta)

        assert Meta.db_table == "test_table"

    def test_indexes(self):
        Index("my_super_index", self.table.c.name)

        Meta = meta.build_meta_class(self.table, self.user_defined_meta)

        assert len(Meta.indexes) == 1

    def test_fail_when_indexes_field_is_overriden(self):
        class Meta:
            indexes = [models.Index(name="bad_index", fields=["some_field"])]

        Index("my_super_index", self.table.c.name)

        with pytest.raises(errors.PolyjuiceError) as err:
            meta.build_meta_class(self.table, Meta)

        assert err.value.args[0] == "You cannot override Meta.indexes field."

    def test_fail_when_db_table_field_is_overriden(self):
        class Meta:
            db_table = "my_custom_name"

        with pytest.raises(errors.PolyjuiceError) as err:
            meta.build_meta_class(self.table, Meta)

        assert err.value.args[0] == "You cannot override Meta.db_table field."

    def test_fail_when_model_is_abstract(self):
        class Meta:
            abstract = True

        with pytest.raises(errors.PolyjuiceError) as err:
            meta.build_meta_class(self.table, Meta)

        assert err.value.args[0] == "You cannot mimic an abstract model."
