# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
                ('basename', models.CharField(max_length=16, unique=True)),
                ('slug', models.CharField(blank=True, max_length=16, unique=True)),
                ('icon', models.ImageField(upload_to='')),
            ],
        ),
    ]
