# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'verbose_name': 'Download Requirement',
                'verbose_name_plural': 'Download Requirements',
            },
        ),
        migrations.CreateModel(
            name='PyPiRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('slug', models.SlugField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': 'PyPi Requirement',
                'verbose_name_plural': 'PyPi Requirements',
            },
        ),
        migrations.CreateModel(
            name='VersionControlRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('vcs_type', models.PositiveSmallIntegerField(choices=[(0, 'git'), (1, 'hg'), (2, 'svn'), (3, 'bzr')], db_index=True, editable=False, help_text='The type of Version Control used in the url.', null=True)),
                ('url', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Version Control Requirement',
                'verbose_name_plural': 'Version Control Requirements',
            },
        ),
    ]
