from django import forms
from .models import Service
from .models import Appointment, Task, Worker


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

class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'worker', 'status', 'deadline']
        
    def __init__(self, *args, **kwargs):
        super(TaskAssignmentForm, self).__init__(*args, **kwargs)
        # Customize form fields if needed
        # For example, you can filter worker choices based on availability or specialization.
        self.fields['worker'].queryset = Worker.objects.filter(is_available=True)  # Filter available workers

