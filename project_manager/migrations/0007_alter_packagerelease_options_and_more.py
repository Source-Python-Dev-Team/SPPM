# Generated by Django 4.0.2 on 2022-03-19 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0006_alter_package_owner_alter_packagerelease_created_by_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='packagerelease',
            options={'verbose_name': 'Package Release', 'verbose_name_plural': 'Package Releases'},
        ),
        migrations.AlterModelOptions(
            name='pluginrelease',
            options={'verbose_name': 'Plugin Release', 'verbose_name_plural': 'Plugin Releases'},
        ),
        migrations.AlterModelOptions(
            name='subpluginrelease',
            options={'verbose_name': 'SubPlugin Release', 'verbose_name_plural': 'SubPlugin Releases'},
        ),
    ]
