# Generated by Django 5.1 on 2024-09-23 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0006_add_field_in_areas'),
    ]

    operations = [
        migrations.AddField(
            model_name='donations',
            name='donations_spent',
            field=models.FloatField(null=True),
        ),
    ]
