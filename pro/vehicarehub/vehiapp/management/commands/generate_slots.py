from django.core.management.base import BaseCommand
from vehiapp.models import Slot
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate slots for a specified date range.'

    def handle(self, *args, **options):
        # Define the date range for which you want to generate slots
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=30)  # Adjust the number of days as needed

        # Define the time slots you want to generate
        time_slots = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']

        # Loop through the date range and time slots to create slots
        for date in daterange(start_date, end_date):
            for time_slot in time_slots:
                slot_datetime = datetime.combine(date, datetime.strptime(time_slot, '%H:%M').time())
                Slot.objects.get_or_create(service_date=date, service_time=slot_datetime)

        self.stdout.write(self.style.SUCCESS('Successfully generated slots.'))

# Function to generate a date range
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)
