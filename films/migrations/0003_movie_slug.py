# Generated by Django 4.1 on 2022-08-18 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_movie_budget_movie_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]