# Generated by Django 4.0.3 on 2022-03-27 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_manager', '0001_initial'),
        ('tags', '0001_initial'),
        ('requirements', '0001_initial'),
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
    ]
