# Generated by Django 3.1.2 on 2021-03-22 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdventureClub', '0011_auto_20210321_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventureevent',
            name='event_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='AdventureClub.adventureclub'),
        ),
    ]
