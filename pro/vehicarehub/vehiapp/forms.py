from django import forms
from .models import Service
from .models import Appointment


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'service_description', 'service_cost', 'service_image']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'service_description': forms.TextInput(attrs={'class': 'form-control'}),
            'service_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'service_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['vehicle_model', 'build_year', 'engine_number', 'chassis_number', 'registration_number', 'service_date', 'service_time', 'service_type']
        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date'}),
            'service_time': forms.TimeInput(attrs={'type': 'time'}),
        }




