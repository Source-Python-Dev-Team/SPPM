# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 23:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumUser',
            fields=[
                ('forum_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='forum_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Forum User',
                'verbose_name_plural': 'Forum Users',
            },
        ),
    ]
