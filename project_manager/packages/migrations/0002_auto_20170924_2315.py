# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 23:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        ('tags', '0001_initial'),
        ('users', '0001_initial'),
        ('packages', '0001_initial'),
        ('requirements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='contributors',
            field=models.ManyToManyField(related_name='package_contributions', to='users.ForumUser'),
        ),
        migrations.AddField(
            model_name='package',
            name='download_requirements',
            field=models.ManyToManyField(related_name='required_in_packages', to='requirements.DownloadRequirement'),
        ),
        migrations.AddField(
            model_name='package',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='users.ForumUser'),
        ),
        migrations.AddField(
            model_name='package',
            name='package_requirements',
            field=models.ManyToManyField(related_name='required_in_packages', to='packages.Package'),
        ),
        migrations.AddField(
            model_name='package',
            name='pypi_requirements',
            field=models.ManyToManyField(related_name='required_in_packages', to='requirements.PyPiRequirement'),
        ),
        migrations.AddField(
            model_name='package',
            name='supported_games',
            field=models.ManyToManyField(related_name='packages', to='games.Game'),
        ),
        migrations.AddField(
            model_name='package',
            name='tags',
            field=models.ManyToManyField(related_name='packages', to='tags.Tag'),
        ),
        migrations.AddField(
            model_name='package',
            name='vcs_requirements',
            field=models.ManyToManyField(related_name='required_in_packages', to='requirements.VersionControlRequirement'),
        ),
    ]
