# Generated by Django 4.2.5 on 2024-03-06 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiapp', '0046_remove_accidentclaim_assigned_to_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='policyrecord',
            name='premium',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
