# Generated by Django 4.2.5 on 2024-02-22 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehiapp', '0038_remove_accidentclaim_document_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accidentclaim',
            name='assigned_worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehiapp.worker'),
        ),
    ]
