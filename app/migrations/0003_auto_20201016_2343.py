# Generated by Django 3.1.2 on 2020-10-16 21:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201014_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='date tracked'),
        ),
    ]