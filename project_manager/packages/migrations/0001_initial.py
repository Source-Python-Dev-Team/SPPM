# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-05 21:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import precise_bbcode.fields
import project_manager.common.helpers
import project_manager.packages.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('requirements', '0001_initial'),
        ('tags', '0001_initial'),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('name', models.CharField(help_text="The name of the project. Do not include the version, as that is added dynamically to the project's page.", max_length=64)),
                ('_configuration_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('configuration', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='The configuration of the project. If too long, post on the forum and provide the link here. BBCode is allowed. 1024 char limit.', max_length=1024, no_rendered_field=True, null=True)),
                ('_description_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('description', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='The full description of the project. BBCode is allowed. 1024 char limit.', max_length=1024, no_rendered_field=True, null=True)),
                ('logo', models.ImageField(blank=True, help_text="The project's logo image.", null=True, upload_to=project_manager.common.helpers.handle_logo_upload)),
                ('_synopsis_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('synopsis', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='A brief description of the project. BBCode is allowed. 128 char limit.', max_length=128, no_rendered_field=True, null=True)),
                ('topic', models.IntegerField(blank=True, null=True, unique=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('basename', models.CharField(blank=True, max_length=32, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][0-9a-z_]*[0-9a-z]')])),
                ('slug', models.SlugField(blank=True, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('contributors', models.ManyToManyField(related_name='package_contributions', to='users.ForumUser')),
                ('download_requirements', models.ManyToManyField(related_name='required_in_packages', to='requirements.DownloadRequirement')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='users.ForumUser')),
                ('package_requirements', models.ManyToManyField(related_name='required_in_packages', to='packages.Package')),
                ('pypi_requirements', models.ManyToManyField(related_name='required_in_packages', to='requirements.PyPiRequirement')),
                ('supported_games', models.ManyToManyField(related_name='packages', to='games.Game')),
                ('tags', models.ManyToManyField(related_name='packages', to='tags.Tag')),
                ('vcs_requirements', models.ManyToManyField(related_name='required_in_packages', to='requirements.VersionControlRequirement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackageImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=project_manager.packages.helpers.handle_package_image_upload)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='packages.Package')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='PackageRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(help_text='The version for this release of the project.', max_length=8, validators=[django.core.validators.RegexValidator('^[0-9][0-9a-z.]*[0-9a-z]')])),
                ('_notes_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('notes', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='The notes for this particular release of the project.', max_length=512, no_rendered_field=True, null=True)),
                ('zip_file', models.FileField(upload_to=project_manager.common.helpers.handle_zip_file_upload)),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='packages.Package')),
            ],
            options={
                'verbose_name': 'Release',
                'verbose_name_plural': 'Releases',
                'abstract': False,
            },
        ),
    ]
