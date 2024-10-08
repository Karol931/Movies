# Generated by Django 4.2.5 on 2024-10-03 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0004_rename_season_id_episodes_season_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episodes',
            name='season',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='media.seasons'),
        ),
        migrations.AlterField(
            model_name='seasons',
            name='tv_show',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='media.tvshows'),
        ),
    ]
