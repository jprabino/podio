# Generated by Django 2.2.2 on 2019-09-22 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llegada', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='place_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='race',
            name='place_long',
            field=models.FloatField(blank=True, null=True),
        ),
    ]