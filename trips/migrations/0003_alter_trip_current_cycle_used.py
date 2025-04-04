# Generated by Django 5.1.7 on 2025-03-14 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_remove_trip_current_cycle_hours_and_more'),
    ]

  # Avant de convertir en double precision, convertissez d'abord en integer
operations = [
    migrations.RunSQL(
        "ALTER TABLE trips_trip ADD COLUMN current_cycle_used_temp integer",
        "ALTER TABLE trips_trip DROP COLUMN current_cycle_used_temp"
    ),
    migrations.RunSQL(
        "UPDATE trips_trip SET current_cycle_used_temp = CASE WHEN current_cycle_used THEN 1 ELSE 0 END",
        ""
    ),
    migrations.RunSQL(
        "ALTER TABLE trips_trip DROP COLUMN current_cycle_used",
        ""
    ),
    migrations.RunSQL(
        "ALTER TABLE trips_trip RENAME COLUMN current_cycle_used_temp TO current_cycle_used",
        ""
    ),
    migrations.AlterField(
        model_name='trip',
        name='current_cycle_used',
        field=models.FloatField(default=0.0),
    ),
]
