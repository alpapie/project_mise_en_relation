# Generated by Django 3.2.4 on 2021-08-11 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_it', '0004_rename_dommaine_mission_domaine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postuler',
            name='date_postula',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]