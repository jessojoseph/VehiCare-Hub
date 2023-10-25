# Generated by Django 4.2.5 on 2023-10-13 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiapp', '0025_alter_appointment_appointment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_model', models.CharField(max_length=100)),
                ('vehicle_year', models.IntegerField()),
                ('mileage', models.IntegerField()),
                ('engine_temperature', models.FloatField()),
                ('oil_level', models.FloatField()),
                ('engine_health', models.CharField(max_length=10)),
                ('oil_quality', models.CharField(max_length=10)),
                ('predicted_service_time', models.FloatField()),
                ('recommended_services', models.TextField()),
            ],
        ),
    ]
