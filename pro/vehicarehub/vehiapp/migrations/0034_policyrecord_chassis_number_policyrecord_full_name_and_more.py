# Generated by Django 4.2.5 on 2024-01-23 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiapp', '0033_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='policyrecord',
            name='chassis_number',
            field=models.CharField(default='****', max_length=100),
        ),
        migrations.AddField(
            model_name='policyrecord',
            name='full_name',
            field=models.CharField(default='****', max_length=255),
        ),
        migrations.AddField(
            model_name='policyrecord',
            name='mob_number',
            field=models.CharField(default='****', max_length=15),
        ),
        migrations.AddField(
            model_name='policyrecord',
            name='purchase_year',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='policyrecord',
            name='rc_number',
            field=models.CharField(default='****', max_length=100),
        ),
        migrations.AddField(
            model_name='policyrecord',
            name='vehicle_number',
            field=models.CharField(default='****', max_length=100),
        ),
    ]
