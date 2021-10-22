# Generated by Django 3.2.8 on 2021-10-22 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0001_initial'),
        ('project_manager', '0001_initial'),
        ('requirements', '0001_initial'),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplugintag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.tag'),
        ),
        migrations.AddField(
            model_name='subpluginreleaseversioncontrolrequirement',
            name='sub_plugin_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.subpluginrelease'),
        ),
        migrations.AddField(
            model_name='subpluginreleaseversioncontrolrequirement',
            name='vcs_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.versioncontrolrequirement'),
        ),
        migrations.AddField(
            model_name='subpluginreleasepypirequirement',
            name='pypi_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.pypirequirement'),
        ),
        migrations.AddField(
            model_name='subpluginreleasepypirequirement',
            name='sub_plugin_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.subpluginrelease'),
        ),
        migrations.AddField(
            model_name='subpluginreleasepackagerequirement',
            name='package_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.package'),
        ),
        migrations.AddField(
            model_name='subpluginreleasepackagerequirement',
            name='sub_plugin_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.subpluginrelease'),
        ),
        migrations.AddField(
            model_name='subpluginreleasedownloadrequirement',
            name='download_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.downloadrequirement'),
        ),
        migrations.AddField(
            model_name='subpluginreleasedownloadrequirement',
            name='sub_plugin_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.subpluginrelease'),
        ),
        migrations.AddField(
            model_name='subpluginrelease',
            name='download_requirements',
            field=models.ManyToManyField(related_name='required_in_sub_plugin_releases', through='project_manager.SubPluginReleaseDownloadRequirement', to='requirements.DownloadRequirement'),
        ),
        migrations.AddField(
            model_name='subpluginrelease',
            name='package_requirements',
            field=models.ManyToManyField(related_name='required_in_sub_plugin_releases', through='project_manager.SubPluginReleasePackageRequirement', to='project_manager.Package'),
        ),
        migrations.AddField(
            model_name='subpluginrelease',
            name='pypi_requirements',
            field=models.ManyToManyField(related_name='required_in_sub_plugin_releases', through='project_manager.SubPluginReleasePyPiRequirement', to='requirements.PyPiRequirement'),
        ),
        migrations.AddField(
            model_name='subpluginrelease',
            name='sub_plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='project_manager.subplugin'),
        ),
        migrations.AddField(
            model_name='subpluginrelease',
            name='vcs_requirements',
            field=models.ManyToManyField(related_name='required_in_sub_plugin_releases', through='project_manager.SubPluginReleaseVersionControlRequirement', to='requirements.VersionControlRequirement'),
        ),
        migrations.AddField(
            model_name='subpluginpath',
            name='plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paths', to='project_manager.plugin'),
        ),
        migrations.AddField(
            model_name='subpluginimage',
            name='sub_plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='project_manager.subplugin'),
        ),
        migrations.AddField(
            model_name='subplugingame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game'),
        ),
        migrations.AddField(
            model_name='subplugingame',
            name='sub_plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.subplugin'),
        ),
        migrations.AddField(
            model_name='subplugincontributor',
            name='sub_plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.subplugin'),
        ),
    ]
