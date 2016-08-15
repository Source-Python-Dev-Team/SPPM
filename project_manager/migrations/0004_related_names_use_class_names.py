# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-14 16:44
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0003_added_topic_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='tags',
            field=models.ManyToManyField(related_name='packages', to='project_manager.Tag'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='tags',
            field=models.ManyToManyField(related_name='plugins', to='project_manager.Tag'),
        ),
        migrations.AddField(
            model_name='subplugin',
            name='tags',
            field=models.ManyToManyField(related_name='subplugins', to='project_manager.Tag'),
        ),
        migrations.AlterField(
            model_name='subplugin',
            name='contributors',
            field=models.ManyToManyField(related_name='subplugin_contributions', to='project_manager.ForumUser'),
        ),
        migrations.AlterField(
            model_name='subplugin',
            name='download_requirements',
            field=models.ManyToManyField(related_name='subplugins', to='project_manager.DownloadRequirement'),
        ),
        migrations.AlterField(
            model_name='subplugin',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subplugins', to='project_manager.ForumUser'),
        ),
        migrations.AlterField(
            model_name='subplugin',
            name='package_requirements',
            field=models.ManyToManyField(related_name='required_in_subplugins', to='project_manager.Package'),
        ),
        migrations.AlterField(
            model_name='subplugin',
            name='pypi_requirements',
            field=models.ManyToManyField(related_name='required_in_subplugins', to='project_manager.PyPiRequirement'),
        ),
        migrations.AlterField(
            model_name='subplugin',
            name='supported_games',
            field=models.ManyToManyField(related_name='subplugins', to='project_manager.Game'),
        ),
        migrations.AlterField(
            model_name='subplugin',
            name='vcs_requirements',
            field=models.ManyToManyField(related_name='subplugins', to='project_manager.VersionControlRequirement'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(b'^[a-z]*')]),
        ),
    ]