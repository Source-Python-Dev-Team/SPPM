# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 12:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import precise_bbcode.fields
import project_manager.plugins.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_manager', '0001_initial'),
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_configuration_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('configuration', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='The configuration of the project. If too long, post on the forum and provide the link here. BBCode is allowed. 1024 char limit.', max_length=1024, no_rendered_field=True, null=True)),
                ('_description_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('description', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='The full description of the project. BBCode is allowed. 1024 char limit.', max_length=1024, no_rendered_field=True, null=True)),
                ('_synopsis_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('synopsis', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='A brief description of the project. BBCode is allowed. 128 char limit.', max_length=128, no_rendered_field=True, null=True)),
                ('topic', models.IntegerField(blank=True, null=True, unique=True)),
                ('name', models.CharField(help_text="The name of the plugin. Do not include the version, as that is added dynamically to the plugin's page.", max_length=64, unique=True)),
                ('basename', models.CharField(blank=True, max_length=32, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][0-9a-z_]*[0-9a-z]')])),
                ('slug', models.SlugField(blank=True, max_length=32, unique=True)),
                ('logo', models.ImageField(blank=True, help_text="The plugin's logo image.", null=True, upload_to=project_manager.plugins.helpers.handle_plugin_logo_upload)),
                ('contributors', models.ManyToManyField(related_name='plugin_contributions', to='project_manager.ForumUser')),
                ('download_requirements', models.ManyToManyField(related_name='plugins', to='project_manager.DownloadRequirement')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plugins', to='project_manager.ForumUser')),
                ('package_requirements', models.ManyToManyField(related_name='required_in_plugins', to='packages.Package')),
                ('pypi_requirements', models.ManyToManyField(related_name='required_in_plugins', to='project_manager.PyPiRequirement')),
                ('supported_games', models.ManyToManyField(related_name='plugins', to='project_manager.Game')),
                ('tags', models.ManyToManyField(related_name='plugins', to='project_manager.Tag')),
                ('vcs_requirements', models.ManyToManyField(related_name='plugins', to='project_manager.VersionControlRequirement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PluginImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=project_manager.plugins.helpers.handle_plugin_image_upload)),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='plugins.Plugin')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='PluginRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('version', models.CharField(help_text='The version for this release of the plugin.', max_length=8, validators=[django.core.validators.RegexValidator('^[0-9][0-9a-z.]*[0-9a-z]')])),
                ('_notes_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('notes', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='The notes for this particular release of the plugin.', max_length=512, no_rendered_field=True, null=True)),
                ('zip_file', models.FileField(upload_to=project_manager.plugins.helpers.handle_plugin_zip_upload)),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='plugins.Plugin')),
            ],
            options={
                'verbose_name': 'Release',
                'verbose_name_plural': 'Releases',
            },
        ),
        migrations.CreateModel(
            name='SubPluginPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator('^[a-z][0-9a-z/\\\\_]*[0-9a-z]')])),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paths', to='plugins.Plugin')),
            ],
            options={
                'verbose_name': 'SubPlugin Path',
                'verbose_name_plural': 'SubPlugin Paths',
            },
        ),
        migrations.AlterUniqueTogether(
            name='subpluginpath',
            unique_together=set([('path', 'plugin')]),
        ),
    ]
