# Generated by Django 4.2.5 on 2024-04-02 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiapp', '0056_roadsideassistancerequest_otp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accidentclaim',
            name='survey_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=10, verbose_name='Survey Status'),
        ),
    ]
