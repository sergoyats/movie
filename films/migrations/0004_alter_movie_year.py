# Generated by Django 4.1 on 2022-08-19 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_movie_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
