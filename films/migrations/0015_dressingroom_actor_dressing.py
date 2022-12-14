# Generated by Django 4.1 on 2022-08-24 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0014_alter_actor_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='DressingRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.IntegerField()),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='actor',
            name='dressing',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='films.dressingroom'),
        ),
    ]
