# Generated by Django 4.2.5 on 2024-10-03 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0005_alter_episodes_season_alter_seasons_tv_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episodes',
            name='season',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='media.seasons'),
        ),
        migrations.AlterField(
            model_name='seasons',
            name='tv_show',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='media.tvshows'),
        ),
    ]
