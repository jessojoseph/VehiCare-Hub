from django import forms
from .models import Service
from .models import Appointment, Task, Worker,Category, Policy, PolicyRecord, Question, UserProfile, CustomUser, AccidentClaim


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
        fields = ['vehicle_model', 'service_date', 'service_type', 'registration_number']
        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date'}),
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


class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name']

class PolicyForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=Category.objects.all(),empty_label="Category Name", to_field_name="id")
    class Meta:
        model=Policy
        fields=['policy_name','sum_assurance','premium','tenure']

class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=['description']
        widgets = {
        'description': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['address','phone_no','profile_pic']


class InsuranceApplicationForm(forms.Form):
    vehicle_number = forms.CharField(label='Vehicle Number', max_length=100)
    purchase_year = forms.IntegerField(label='Purchase Year')
    full_name = forms.CharField(label='Full Name', max_length=255)
    mob_number = forms.CharField(label='Mobile Number', max_length=15)
    rc_number = forms.CharField(label='RC Number', max_length=100)
    chassis_number = forms.CharField(label='Chassis Number', max_length=100)


class AccidentClaimForm(forms.ModelForm):
    class Meta:
        model = AccidentClaim
        fields = ['incident_type', 'incident_date', 'description', 'document']
