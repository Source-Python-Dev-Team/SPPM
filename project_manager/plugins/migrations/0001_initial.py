# Generated by Django 3.2.8 on 2021-10-22 13:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import embed_video.fields
import model_utils.fields
import precise_bbcode.fields
import project_manager.common.helpers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('packages', '0001_initial'),
        ('games', '0001_initial'),
        ('requirements', '0001_initial'),
        ('users', '0001_initial'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('name', models.CharField(help_text="The name of the project. Do not include the version, as that is added dynamically to the project's page.", max_length=64)),
                ('_configuration_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('configuration', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='The configuration of the project. If too long, post on the forum and provide the link here. BBCode is allowed. 1024 char limit.', max_length=1024, no_rendered_field=True, null=True)),
                ('_description_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('description', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='The full description of the project. BBCode is allowed. 1024 char limit.', max_length=1024, no_rendered_field=True, null=True)),
                ('logo', models.ImageField(blank=True, help_text="The project's logo image.", null=True, upload_to=project_manager.common.helpers.handle_project_logo_upload)),
                ('video', embed_video.fields.EmbedVideoField(help_text="The project's video.", null=True)),
                ('_synopsis_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('synopsis', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='A brief description of the project. BBCode is allowed. 128 char limit.', max_length=128, no_rendered_field=True, null=True)),
                ('topic', models.IntegerField(blank=True, null=True, unique=True)),
                ('created', models.DateTimeField(verbose_name='created')),
                ('updated', models.DateTimeField(verbose_name='updated')),
                ('basename', models.CharField(blank=True, max_length=32, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][0-9a-z_]*[0-9a-z]')])),
                ('slug', models.SlugField(blank=True, max_length=32, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PluginRelease',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(help_text='The version for this release of the project.', max_length=8, validators=[django.core.validators.RegexValidator('^[0-9][0-9a-z.]*[0-9a-z]')])),
                ('_notes_rendered', models.TextField(blank=True, editable=False, null=True)),
                ('notes', precise_bbcode.fields.BBCodeTextField(blank=True, help_text='The notes for this particular release of the project.', max_length=512, no_rendered_field=True, null=True)),
                ('zip_file', models.FileField(upload_to=project_manager.common.helpers.handle_release_zip_file_upload)),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
            ],
            options={
                'verbose_name': 'Release',
                'verbose_name_plural': 'Releases',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PluginTag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plugins.plugin')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.tag')),
            ],
            options={
                'unique_together': {('plugin', 'tag')},
            },
        ),
        migrations.CreateModel(
            name='PluginReleaseVersionControlRequirement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(blank=True, help_text='The version of the VCS package for this release of the project.', max_length=8, null=True, validators=[django.core.validators.RegexValidator('^[0-9][0-9a-z.]*[0-9a-z]')])),
                ('optional', models.BooleanField(default=False)),
                ('plugin_release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plugins.pluginrelease')),
                ('vcs_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.versioncontrolrequirement')),
            ],
            options={
                'unique_together': {('plugin_release', 'vcs_requirement')},
            },
        ),
        migrations.CreateModel(
            name='PluginReleasePyPiRequirement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(blank=True, help_text='The version of the PyPi package for this release of the project.', max_length=8, null=True, validators=[django.core.validators.RegexValidator('^[0-9][0-9a-z.]*[0-9a-z]')])),
                ('optional', models.BooleanField(default=False)),
                ('plugin_release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plugins.pluginrelease')),
                ('pypi_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.pypirequirement')),
            ],
            options={
                'unique_together': {('plugin_release', 'pypi_requirement')},
            },
        ),
        migrations.CreateModel(
            name='PluginReleasePackageRequirement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(blank=True, help_text='The version of the custom package for this release of the project.', max_length=8, null=True, validators=[django.core.validators.RegexValidator('^[0-9][0-9a-z.]*[0-9a-z]')])),
                ('optional', models.BooleanField(default=False)),
                ('package_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.package')),
                ('plugin_release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plugins.pluginrelease')),
            ],
            options={
                'unique_together': {('plugin_release', 'package_requirement')},
            },
        ),
        migrations.CreateModel(
            name='PluginReleaseDownloadRequirement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('optional', models.BooleanField(default=False)),
                ('download_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.downloadrequirement')),
                ('plugin_release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plugins.pluginrelease')),
            ],
            options={
                'unique_together': {('plugin_release', 'download_requirement')},
            },
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='download_requirements',
            field=models.ManyToManyField(related_name='required_in_plugin_releases', through='plugins.PluginReleaseDownloadRequirement', to='requirements.DownloadRequirement'),
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='package_requirements',
            field=models.ManyToManyField(related_name='required_in_plugin_releases', through='plugins.PluginReleasePackageRequirement', to='packages.Package'),
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='plugins.plugin'),
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='pypi_requirements',
            field=models.ManyToManyField(related_name='required_in_plugin_releases', through='plugins.PluginReleasePyPiRequirement', to='requirements.PyPiRequirement'),
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='vcs_requirements',
            field=models.ManyToManyField(related_name='required_in_plugin_releases', through='plugins.PluginReleaseVersionControlRequirement', to='requirements.VersionControlRequirement'),
        ),
        migrations.CreateModel(
            name='PluginImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=project_manager.common.helpers.handle_project_image_upload)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='plugins.plugin')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PluginGame',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plugins.plugin')),
            ],
            options={
                'unique_together': {('plugin', 'game')},
            },
        ),
        migrations.CreateModel(
            name='PluginContributor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plugins.plugin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.forumuser')),
            ],
            options={
                'unique_together': {('plugin', 'user')},
            },
        ),
        migrations.AddField(
            model_name='plugin',
            name='contributors',
            field=models.ManyToManyField(related_name='plugin_contributions', through='plugins.PluginContributor', to='users.ForumUser'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plugins', to='users.forumuser'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='supported_games',
            field=models.ManyToManyField(related_name='plugins', through='plugins.PluginGame', to='games.Game'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='tags',
            field=models.ManyToManyField(related_name='plugins', through='plugins.PluginTag', to='tags.Tag'),
        ),
        migrations.CreateModel(
            name='SubPluginPath',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=256, validators=[django.core.validators.RegexValidator('^[a-z][0-9a-z/\\\\_]*[0-9a-z]')])),
                ('allow_module', models.BooleanField(default=False)),
                ('allow_package_using_basename', models.BooleanField(default=False)),
                ('allow_package_using_init', models.BooleanField(default=False)),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paths', to='plugins.plugin')),
            ],
            options={
                'verbose_name': 'SubPlugin Path',
                'verbose_name_plural': 'SubPlugin Paths',
                'unique_together': {('path', 'plugin')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='pluginrelease',
            unique_together={('plugin', 'version')},
        ),
    ]
