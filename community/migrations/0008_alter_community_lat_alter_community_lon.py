# Generated by Django 4.0.3 on 2022-06-26 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_community_addr21_community_zip21_community_zip22'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='lat',
            field=models.FloatField(default=34.700559, max_length=20),
        ),
        migrations.AlterField(
            model_name='community',
            name='lon',
            field=models.FloatField(default=135.495734, max_length=20),
        ),
    ]
