# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-16 21:02
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import project_manager.packages.helpers
import project_manager.plugins.helpers
import project_manager.sub_plugins.helpers
import precise_bbcode.fields


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
        ),
        migrations.CreateModel(
            name='ForumUser',
            fields=[
                ('username', models.CharField(max_length=30, unique=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
                ('basename', models.CharField(max_length=16, unique=True)),
                ('slug', models.CharField(blank=True, max_length=16, unique=True)),
                ('icon', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_synopsis_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('synopsis', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=128, no_rendered_field=True, null=True)),
                ('_description_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('description', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=1024, no_rendered_field=True, null=True)),
                ('_configuration_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('configuration', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=1024, no_rendered_field=True, null=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('basename', models.CharField(blank=True, max_length=32, unique=True, validators=[django.core.validators.RegexValidator(b'^[a-z][0-9a-z_]*[0-9a-z]')])),
                ('slug', models.SlugField(blank=True, max_length=32, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=project_manager.packages.helpers.handle_package_logo_upload)),
                ('contributors', models.ManyToManyField(related_name='package_contributions', to='project_manager.ForumUser')),
                ('download_requirements', models.ManyToManyField(related_name='packages', to='project_manager.DownloadRequirement')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='project_manager.ForumUser')),
                ('package_requirements', models.ManyToManyField(related_name='required_in_packages', to='project_manager.Package')),
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
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='project_manager.Package')),
            ],
            options={
                'verbose_name': 'Image (Package)',
                'verbose_name_plural': 'Images (Package)',
            },
        ),
        migrations.CreateModel(
            name='PackageRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('version', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(b'^[0-9][0-9a-z.]*[0-9a-z]')])),
                ('_notes_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('notes', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=512, no_rendered_field=True, null=True)),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('zip_file', models.FileField(upload_to=project_manager.packages.helpers.handle_package_zip_upload)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='project_manager.Package')),
            ],
            options={
                'verbose_name': 'Release (Package)',
                'verbose_name_plural': 'Releases (Package)',
            },
        ),
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_synopsis_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('synopsis', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=128, no_rendered_field=True, null=True)),
                ('_description_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('description', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=1024, no_rendered_field=True, null=True)),
                ('_configuration_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('configuration', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=1024, no_rendered_field=True, null=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('basename', models.CharField(blank=True, max_length=32, unique=True, validators=[django.core.validators.RegexValidator(b'^[a-z][0-9a-z_]*[0-9a-z]')])),
                ('slug', models.SlugField(blank=True, max_length=32, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=project_manager.plugins.helpers.handle_plugin_logo_upload)),
                ('contributors', models.ManyToManyField(related_name='plugin_contributions', to='project_manager.ForumUser')),
                ('download_requirements', models.ManyToManyField(related_name='plugins', to='project_manager.DownloadRequirement')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plugins', to='project_manager.ForumUser')),
                ('package_requirements', models.ManyToManyField(related_name='required_in_plugins', to='project_manager.Package')),
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
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='project_manager.Plugin')),
            ],
            options={
                'verbose_name': 'Image (Plugin)',
                'verbose_name_plural': 'Images (Plugin)',
            },
        ),
        migrations.CreateModel(
            name='PluginRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('version', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(b'^[0-9][0-9a-z.]*[0-9a-z]')])),
                ('_notes_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('notes', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=512, no_rendered_field=True, null=True)),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('zip_file', models.FileField(upload_to=project_manager.plugins.helpers.handle_plugin_zip_upload)),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='project_manager.Plugin')),
            ],
            options={
                'verbose_name': 'Release (Plugin)',
                'verbose_name_plural': 'Releases (Plugin)',
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
            name='SubPlugin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_synopsis_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('synopsis', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=128, no_rendered_field=True, null=True)),
                ('_description_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('description', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=1024, no_rendered_field=True, null=True)),
                ('_configuration_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('configuration', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=1024, no_rendered_field=True, null=True)),
                ('name', models.CharField(max_length=64)),
                ('basename', models.CharField(blank=True, max_length=32, validators=[django.core.validators.RegexValidator(b'^[a-z][0-9a-z_]*[0-9a-z]')])),
                ('slug', models.SlugField(blank=True, max_length=32)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=project_manager.sub_plugins.helpers.handle_sub_plugin_logo_upload)),
                ('contributors', models.ManyToManyField(related_name='sub_plugin_contributions', to='project_manager.ForumUser')),
                ('download_requirements', models.ManyToManyField(related_name='sub_plugins', to='project_manager.DownloadRequirement')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_plugins', to='project_manager.ForumUser')),
                ('package_requirements', models.ManyToManyField(related_name='required_in_sub_plugins', to='project_manager.Package')),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_plugins', to='project_manager.Plugin')),
                ('pypi_requirements', models.ManyToManyField(related_name='required_in_sub_plugins', to='project_manager.PyPiRequirement')),
                ('supported_games', models.ManyToManyField(related_name='sub_plugins', to='project_manager.Game')),
            ],
            options={
                'verbose_name': 'SubPlugin',
                'verbose_name_plural': 'SubPlugins',
            },
        ),
        migrations.CreateModel(
            name='SubPluginImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=project_manager.sub_plugins.helpers.handle_sub_plugin_image_upload)),
                ('sub_plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='project_manager.SubPlugin')),
            ],
            options={
                'verbose_name': 'Image (SubPlugin)',
                'verbose_name_plural': 'Images (SubPlugin)',
            },
        ),
        migrations.CreateModel(
            name='SubPluginPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator(b'^[a-z][0-9a-z/\\\\_]*[0-9a-z]')])),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paths', to='project_manager.Plugin')),
            ],
            options={
                'verbose_name': 'SubPlugin path (Plugin)',
                'verbose_name_plural': 'SubPlugin paths (Plugin)',
            },
        ),
        migrations.CreateModel(
            name='SubPluginRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('version', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(b'^[0-9][0-9a-z.]*[0-9a-z]')])),
                ('_notes_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('notes', precise_bbcode.fields.BBCodeTextField(blank=True, max_length=512, no_rendered_field=True, null=True)),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('zip_file', models.FileField(upload_to=project_manager.sub_plugins.helpers.handle_sub_plugin_zip_upload)),
                ('sub_plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='project_manager.SubPlugin')),
            ],
            options={
                'verbose_name': 'Release (SubPlugin)',
                'verbose_name_plural': 'Releases (SubPlugin)',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='VersionControlRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='subplugin',
            name='vcs_requirements',
            field=models.ManyToManyField(related_name='sub_plugins', to='project_manager.VersionControlRequirement'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='pypi_requirements',
            field=models.ManyToManyField(related_name='required_in_plugins', to='project_manager.PyPiRequirement'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='supported_games',
            field=models.ManyToManyField(related_name='plugins', to='project_manager.Game'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='vcs_requirements',
            field=models.ManyToManyField(related_name='plugins', to='project_manager.VersionControlRequirement'),
        ),
        migrations.AddField(
            model_name='package',
            name='pypi_requirements',
            field=models.ManyToManyField(related_name='required_in_packages', to='project_manager.PyPiRequirement'),
        ),
        migrations.AddField(
            model_name='package',
            name='supported_games',
            field=models.ManyToManyField(related_name='packages', to='project_manager.Game'),
        ),
        migrations.AddField(
            model_name='package',
            name='vcs_requirements',
            field=models.ManyToManyField(related_name='packages', to='project_manager.VersionControlRequirement'),
        ),
        migrations.AlterUniqueTogether(
            name='subpluginpath',
            unique_together=set([('path', 'plugin')]),
        ),
        migrations.AlterUniqueTogether(
            name='subplugin',
            unique_together=set([('plugin', 'slug'), ('plugin', 'name'), ('plugin', 'basename')]),
        ),
    ]
