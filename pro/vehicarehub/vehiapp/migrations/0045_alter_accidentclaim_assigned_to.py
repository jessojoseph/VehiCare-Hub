# Generated by Django 4.2.5 on 2024-02-26 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehiapp', '0044_alter_surveyor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accidentclaim',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehiapp.surveyor'),
        ),
    ]
