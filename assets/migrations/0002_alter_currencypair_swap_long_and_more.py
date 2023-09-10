# Generated by Django 4.2.5 on 2023-09-10 14:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("assets", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currencypair",
            name="swap_long",
            field=models.FloatField(
                default=0.0,
                help_text="In-points overnight interest for a long position",
            ),
        ),
        migrations.AlterField(
            model_name="currencypair",
            name="swap_short",
            field=models.FloatField(
                default=0.0,
                help_text="In-points overnight interest for a short position",
            ),
        ),
    ]