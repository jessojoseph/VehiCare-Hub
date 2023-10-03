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

    ROLE_CHOICES = (
        (WORKER, 'Worker'),
        (CUSTOMER, 'Customer'),
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

    appointment_status = models.CharField(max_length=50, default='Scheduled')

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
    audio_file = models.FileField(upload_to='audio_recordings/', null=True)

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