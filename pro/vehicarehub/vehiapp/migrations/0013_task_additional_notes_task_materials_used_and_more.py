# Generated by Django 4.2.5 on 2023-09-20 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiapp', '0012_task_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='additional_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='materials_used',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='work_done',
            field=models.TextField(blank=True, null=True),
        ),
    ]
