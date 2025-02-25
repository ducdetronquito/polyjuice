# Generated by Django 2.2.14 on 2020-07-19 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("houses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Professor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                (
                    "favourite_house",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="houses.House"
                    ),
                ),
            ],
            options={"db_table": "professors__professor",},
        ),
    ]
