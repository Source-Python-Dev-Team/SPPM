# Generated by Django 4.0.3 on 2022-03-27 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='creator',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tags', to='users.forumuser'),
        ),
    ]
