# Generated by Django 4.2.5 on 2024-10-03 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0009_alter_episodes_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episodes',
            name='season',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='media.seasons'),
        ),
    ]
