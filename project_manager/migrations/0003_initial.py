# Generated by Django 3.2.8 on 2021-10-22 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0001_initial'),
        ('users', '0001_initial'),
        ('requirements', '0001_initial'),
        ('project_manager', '0002_initial'),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplugincontributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.forumuser'),
        ),
        migrations.AddField(
            model_name='subplugin',
            name='contributors',
            field=models.ManyToManyField(related_name='subplugin_contributions', through='project_manager.SubPluginContributor', to='users.ForumUser'),
        ),
        migrations.AddField(
            model_name='subplugin',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subplugins', to='users.forumuser'),
        ),
        migrations.AddField(
            model_name='subplugin',
            name='plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_plugins', to='project_manager.plugin'),
        ),
        migrations.AddField(
            model_name='subplugin',
            name='supported_games',
            field=models.ManyToManyField(related_name='subplugins', through='project_manager.SubPluginGame', to='games.Game'),
        ),
        migrations.AddField(
            model_name='subplugin',
            name='tags',
            field=models.ManyToManyField(related_name='subplugins', through='project_manager.SubPluginTag', to='tags.Tag'),
        ),
        migrations.AddField(
            model_name='plugintag',
            name='plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.plugin'),
        ),
        migrations.AddField(
            model_name='plugintag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.tag'),
        ),
        migrations.AddField(
            model_name='pluginreleaseversioncontrolrequirement',
            name='plugin_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.pluginrelease'),
        ),
        migrations.AddField(
            model_name='pluginreleaseversioncontrolrequirement',
            name='vcs_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.versioncontrolrequirement'),
        ),
        migrations.AddField(
            model_name='pluginreleasepypirequirement',
            name='plugin_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.pluginrelease'),
        ),
        migrations.AddField(
            model_name='pluginreleasepypirequirement',
            name='pypi_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.pypirequirement'),
        ),
        migrations.AddField(
            model_name='pluginreleasepackagerequirement',
            name='package_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.package'),
        ),
        migrations.AddField(
            model_name='pluginreleasepackagerequirement',
            name='plugin_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.pluginrelease'),
        ),
        migrations.AddField(
            model_name='pluginreleasedownloadrequirement',
            name='download_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.downloadrequirement'),
        ),
        migrations.AddField(
            model_name='pluginreleasedownloadrequirement',
            name='plugin_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.pluginrelease'),
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='download_requirements',
            field=models.ManyToManyField(related_name='required_in_plugin_releases', through='project_manager.PluginReleaseDownloadRequirement', to='requirements.DownloadRequirement'),
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='package_requirements',
            field=models.ManyToManyField(related_name='required_in_plugin_releases', through='project_manager.PluginReleasePackageRequirement', to='project_manager.Package'),
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='project_manager.plugin'),
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='pypi_requirements',
            field=models.ManyToManyField(related_name='required_in_plugin_releases', through='project_manager.PluginReleasePyPiRequirement', to='requirements.PyPiRequirement'),
        ),
        migrations.AddField(
            model_name='pluginrelease',
            name='vcs_requirements',
            field=models.ManyToManyField(related_name='required_in_plugin_releases', through='project_manager.PluginReleaseVersionControlRequirement', to='requirements.VersionControlRequirement'),
        ),
        migrations.AddField(
            model_name='pluginimage',
            name='plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='project_manager.plugin'),
        ),
        migrations.AddField(
            model_name='plugingame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game'),
        ),
        migrations.AddField(
            model_name='plugingame',
            name='plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.plugin'),
        ),
        migrations.AddField(
            model_name='plugincontributor',
            name='plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.plugin'),
        ),
        migrations.AddField(
            model_name='plugincontributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.forumuser'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='contributors',
            field=models.ManyToManyField(related_name='plugin_contributions', through='project_manager.PluginContributor', to='users.ForumUser'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plugins', to='users.forumuser'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='supported_games',
            field=models.ManyToManyField(related_name='plugins', through='project_manager.PluginGame', to='games.Game'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='tags',
            field=models.ManyToManyField(related_name='plugins', through='project_manager.PluginTag', to='tags.Tag'),
        ),
        migrations.AddField(
            model_name='packagetag',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.package'),
        ),
        migrations.AddField(
            model_name='packagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.tag'),
        ),
        migrations.AddField(
            model_name='packagereleaseversioncontrolrequirement',
            name='package_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.packagerelease'),
        ),
        migrations.AddField(
            model_name='packagereleaseversioncontrolrequirement',
            name='vcs_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.versioncontrolrequirement'),
        ),
        migrations.AddField(
            model_name='packagereleasepypirequirement',
            name='package_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.packagerelease'),
        ),
        migrations.AddField(
            model_name='packagereleasepypirequirement',
            name='pypi_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.pypirequirement'),
        ),
        migrations.AddField(
            model_name='packagereleasepackagerequirement',
            name='package_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.packagerelease'),
        ),
        migrations.AddField(
            model_name='packagereleasepackagerequirement',
            name='package_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.package'),
        ),
        migrations.AddField(
            model_name='packagereleasedownloadrequirement',
            name='download_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requirements.downloadrequirement'),
        ),
        migrations.AddField(
            model_name='packagereleasedownloadrequirement',
            name='package_release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.packagerelease'),
        ),
        migrations.AddField(
            model_name='packagerelease',
            name='download_requirements',
            field=models.ManyToManyField(related_name='required_in_package_releases', through='project_manager.PackageReleaseDownloadRequirement', to='requirements.DownloadRequirement'),
        ),
        migrations.AddField(
            model_name='packagerelease',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='project_manager.package'),
        ),
        migrations.AddField(
            model_name='packagerelease',
            name='package_requirements',
            field=models.ManyToManyField(related_name='required_in_package_releases', through='project_manager.PackageReleasePackageRequirement', to='project_manager.Package'),
        ),
        migrations.AddField(
            model_name='packagerelease',
            name='pypi_requirements',
            field=models.ManyToManyField(related_name='required_in_package_releases', through='project_manager.PackageReleasePyPiRequirement', to='requirements.PyPiRequirement'),
        ),
        migrations.AddField(
            model_name='packagerelease',
            name='vcs_requirements',
            field=models.ManyToManyField(related_name='required_in_package_releases', through='project_manager.PackageReleaseVersionControlRequirement', to='requirements.VersionControlRequirement'),
        ),
        migrations.AddField(
            model_name='packageimage',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='project_manager.package'),
        ),
        migrations.AddField(
            model_name='packagegame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game'),
        ),
        migrations.AddField(
            model_name='packagegame',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.package'),
        ),
        migrations.AddField(
            model_name='packagecontributor',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.package'),
        ),
        migrations.AddField(
            model_name='packagecontributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.forumuser'),
        ),
        migrations.AddField(
            model_name='package',
            name='contributors',
            field=models.ManyToManyField(related_name='package_contributions', through='project_manager.PackageContributor', to='users.ForumUser'),
        ),
        migrations.AddField(
            model_name='package',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='users.forumuser'),
        ),
        migrations.AddField(
            model_name='package',
            name='supported_games',
            field=models.ManyToManyField(related_name='packages', through='project_manager.PackageGame', to='games.Game'),
        ),
        migrations.AddField(
            model_name='package',
            name='tags',
            field=models.ManyToManyField(related_name='packages', through='project_manager.PackageTag', to='tags.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='subplugintag',
            unique_together={('sub_plugin', 'tag')},
        ),
        migrations.AlterUniqueTogether(
            name='subpluginreleaseversioncontrolrequirement',
            unique_together={('sub_plugin_release', 'vcs_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='subpluginreleasepypirequirement',
            unique_together={('sub_plugin_release', 'pypi_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='subpluginreleasepackagerequirement',
            unique_together={('sub_plugin_release', 'package_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='subpluginreleasedownloadrequirement',
            unique_together={('sub_plugin_release', 'download_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='subpluginpath',
            unique_together={('path', 'plugin')},
        ),
        migrations.AlterUniqueTogether(
            name='subplugingame',
            unique_together={('sub_plugin', 'game')},
        ),
        migrations.AlterUniqueTogether(
            name='subplugincontributor',
            unique_together={('sub_plugin', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='subplugin',
            unique_together={('plugin', 'slug'), ('plugin', 'basename'), ('plugin', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='plugintag',
            unique_together={('plugin', 'tag')},
        ),
        migrations.AlterUniqueTogether(
            name='pluginreleaseversioncontrolrequirement',
            unique_together={('plugin_release', 'vcs_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='pluginreleasepypirequirement',
            unique_together={('plugin_release', 'pypi_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='pluginreleasepackagerequirement',
            unique_together={('plugin_release', 'package_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='pluginreleasedownloadrequirement',
            unique_together={('plugin_release', 'download_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='pluginrelease',
            unique_together={('plugin', 'version')},
        ),
        migrations.AlterUniqueTogether(
            name='plugingame',
            unique_together={('plugin', 'game')},
        ),
        migrations.AlterUniqueTogether(
            name='plugincontributor',
            unique_together={('plugin', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='packagetag',
            unique_together={('package', 'tag')},
        ),
        migrations.AlterUniqueTogether(
            name='packagereleaseversioncontrolrequirement',
            unique_together={('package_release', 'vcs_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='packagereleasepypirequirement',
            unique_together={('package_release', 'pypi_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='packagereleasepackagerequirement',
            unique_together={('package_release', 'package_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='packagereleasedownloadrequirement',
            unique_together={('package_release', 'download_requirement')},
        ),
        migrations.AlterUniqueTogether(
            name='packagegame',
            unique_together={('package', 'game')},
        ),
        migrations.AlterUniqueTogether(
            name='packagecontributor',
            unique_together={('package', 'user')},
        ),
    ]
