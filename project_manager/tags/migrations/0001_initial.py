# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 20:48
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=16, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator('^[a-z]*')])),
                ('black_listed', models.BooleanField(default=False)),
            ],
        ),
    ]
