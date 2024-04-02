from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.db import models
from datetime import time

current_datetime = timezone.now()


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name, last_name, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(first_name, last_name, username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    WORKER = 1
    CUSTOMER = 2
    ADVISOR = 3
    SURVEYOR = 4

    ROLE_CHOICES = (
        (WORKER, 'Worker'),
        (CUSTOMER, 'Customer'),
        (ADVISOR, 'Advisor'),
        (SURVEYOR, 'Surveyor'),


    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.username


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    service_description = models.TextField()
    service_cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_image = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.service_name

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.FileField(upload_to='profile_photo/', blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=15, blank=True, null=True)
    phone_no = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # Corrected method name using double underscores
        if self.user:
            return self.user.username
        else:
            return "UserProfile with no associated user"
        
class Worker(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    specialized_service = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(null=True)
    is_available = models.BooleanField(default=True) 


    def __str__(self):
        return self.user.username
    
class Slot(models.Model):
    service_date = models.DateField()
    service_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service_date} {self.service_time}"



class Appointment(models.Model):
    user_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=100)
    service_date = models.DateField()
    service_time = models.TimeField(default=time(0, 0, 0))
    service_type = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    registration_number = models.CharField(max_length=100)

    APPOINTMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
    ]

    appointment_status = models.CharField(
        max_length=50,
        choices=APPOINTMENT_STATUS_CHOICES,
        default='Pending',
    )

    def __str__(self):
        return f"{self.user_name}'s Appointment on {self.service_date} for {self.vehicle_model}"


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')])
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    work_done = models.TextField(blank=True, null=True)
    materials_used = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
    recognized_text = models.TextField(blank=True, null=True)



    def __str__(self):
        return self.title

class AudioRecording(models.Model):
    audio_file = models.FileField(upload_to='audio_recordings/')  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, default=None)  # Add this field
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)  # Provide a default value here

    def __str__(self):
        return self.audio_file.name



class LeaveRequest(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

    def __str__(self):
        return f"{self.worker.user.username}'s Leave Request"

class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
         
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the payment to a user
    razorpay_order_id = models.CharField(max_length=255)  # Razorpay order ID
    payment_id = models.CharField(max_length=255)  # Razorpay payment ID
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Amount paid
    currency = models.CharField(max_length=5)  # Currency code (e.g., "INR")
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)


    def str(self):
        return f"Payment for {self.appointment}"

    class Meta:
        ordering = ['-timestamp']

#Update Status not implemented
    def update_status(self):
        # Calculate the time difference in minutes
        time_difference = (timezone.now() - self.timestamp).total_seconds() / 60

        if self.payment_status == self.PaymentStatusChoices.PENDING and time_difference > 1:
            # Update the status to "Failed"
            self.payment_status = self.PaymentStatusChoices.FAILED
            self.save()


class ServicePrediction(models.Model):
    vehicle_model = models.CharField(max_length=100)
    vehicle_year = models.IntegerField()
    mileage = models.IntegerField()
    engine_temperature = models.FloatField()
    oil_level = models.FloatField()
    engine_health = models.CharField(max_length=10)
    oil_quality = models.CharField(max_length=10)
    predicted_service_time = models.FloatField()
    recommended_services = models.TextField()

    def __str__(self):
        return self.vehicle_model


class ServiceTimePrediction(models.Model):
    bike_model = models.CharField(max_length=255)
    age = models.IntegerField()
    service_type = models.CharField(max_length=255)
    service_history = models.IntegerField()
    build_year = models.IntegerField()
    mileage = models.IntegerField()
    last_serviced_date = models.IntegerField()
    current_year = models.IntegerField()
    predicted_time = models.IntegerField()

    def __str__(self):
        return f"ServiceTimePrediction {self.id}"

class Advisor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(null=True)
    is_available = models.BooleanField(default=True) 


    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    category_name =models.CharField(max_length=20)
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.category_name
    

class Policy(models.Model):
    category= models.ForeignKey('Category', on_delete=models.CASCADE)
    policy_name=models.CharField(max_length=200)
    sum_assurance=models.PositiveIntegerField()
    premium=models.PositiveIntegerField()
    tenure=models.PositiveIntegerField()
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.policy_name

class PolicyRecord(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Pending')
    creation_date = models.DateField(auto_now=True)

    vehicle_number = models.CharField(max_length=100, default='****')
    purchase_year = models.IntegerField(default=20)
    full_name = models.CharField(max_length=255, default='****')
    mob_number = models.CharField(max_length=15, default='****')
    rc_number = models.CharField(max_length=100, default='****')
    chassis_number = models.CharField(max_length=100, default='****')

    # Fields for premium calculation
    bike_model = models.CharField(max_length=255, default='****')
    bike_make = models.CharField(max_length=255, default='****')
    engine_capacity = models.IntegerField(default=100)
    owner_age = models.IntegerField(default=30)
    owner_gender = models.CharField(max_length=10, default='Male')
    riding_experience = models.IntegerField(default=5)
    voluntary_deductible = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    has_previous_claim = models.BooleanField(default=False)
    add_ons = models.CharField(max_length=255, default='', blank=True)

    # Premium and IDV fields
    premium = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    idv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.Policy.policy_name} - {self.customer.username}"
    
class Question(models.Model):
    customer= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description =models.CharField(max_length=500)
    admin_comment=models.CharField(max_length=200,default='Nothing')
    asked_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.description

class Surveyor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)  # Make it optional
    experience = models.PositiveIntegerField(null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
class AccidentClaim(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    SURVEY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    incident_type = models.CharField(max_length=100)
    incident_date = models.DateField()
    description = models.TextField()
    fir_document = models.FileField(upload_to='accident_claims/', blank=True, null=True, verbose_name='FIR Document')
    dl_document = models.FileField(upload_to='accident_claims/', blank=True, null=True, verbose_name='Driving Licence Document')
    rc_document = models.FileField(upload_to='accident_claims/', blank=True, null=True, verbose_name='Registration Certificate Document')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_assigned = models.BooleanField(default=False)
    assigned_advisor = models.ForeignKey(Advisor, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_advisor')
    assigned_surveyor = models.ForeignKey(Surveyor, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_surveyor')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    rejection_reason = models.TextField(blank=True, null=True)

    survey_status = models.CharField(max_length=10, choices=SURVEY_STATUS_CHOICES, default='Pending', verbose_name='Survey Status')

    policy_record = models.ForeignKey(PolicyRecord, on_delete=models.SET_NULL, null=True, blank=True)


class RoadsideAssistanceRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=50)
    complaint = models.TextField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, default=0.0, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, default=0.0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    otp = models.CharField(max_length=100, default='Null')
    verified = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.name}'s Roadside Assistance Request"


        