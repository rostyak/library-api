# Generated by Django 4.1.3 on 2022-11-30 11:28


import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrow", "0002_borrowing_days_to_return"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="expected_return_date",
            field=models.DateField(default=datetime.date(2022, 12, 10), null=True),
        ),
    ]
