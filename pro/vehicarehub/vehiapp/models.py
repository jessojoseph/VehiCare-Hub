from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


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

class Appointment(models.Model):
    user_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    vehicle_model = models.CharField(max_length=100, default='Yamaha')
    build_year = models.IntegerField(default=2023)
    engine_number = models.CharField(max_length=100, default='')
    chassis_number = models.CharField(max_length=100, default='')
    registration_number = models.CharField(max_length=100, default='')
    service_date = models.DateField(default=timezone.now)
    service_time = models.TimeField(default=datetime.time(0, 0))
    service_type = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user_name)

