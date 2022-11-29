# Generated by Django 4.1.3 on 2022-11-29 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(auto_now_add=True)),
                ('expected_return_date', models.DateField(default=datetime.date(2022, 12, 9), null=True)),
                ('actual_return_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]