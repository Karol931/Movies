# Generated by Django 4.2.5 on 2024-10-07 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0012_servers'),
    ]

    operations = [
        migrations.AddField(
            model_name='servers',
            name='name',
            field=models.CharField(default='a', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
