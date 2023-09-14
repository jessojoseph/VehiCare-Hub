from .forms import AppointmentForm
from .forms import ServiceForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .models import Service, UserProfile
from .models import Service, UserProfile
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from django.urls import reverse
from .models import Service
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import CustomUser
from .models import Worker
from .models import Workerprofile


User = get_user_model()

@login_required
def change_password_client(request):
    val = 0
    
    if request.method == 'POST':
        # Get the current user
        user = User.objects.get(email=request.user.email)
        
        # Get the new password and confirm password from the request
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords are empty
        if not new_password or not confirm_password:
            val = 2  # Passwords are empty
        else:
            # Check if the passwords match
            if new_password == confirm_password:
                # Change the user's password
                user.set_password(new_password)
                user.save()
                # Update the session and log the user back in
                update_session_auth_hash(request, user)
                val = 1  # Password change is successful
            else:
                val = 0  # Passwords do not match
    
    return render(request, 'change_password.html', {'msg': val})


def service_detail(request, service_id):
    # Retrieve the service object using the 'service_id' parameter
    service = get_object_or_404(Service, pk=service_id)
    
    # Render the service detail template with the 'service' object
    return render(request, 'service_detail.html', {'service': service})

def search_view(request):
    if 'q' in request.GET:
        query = request.GET['q']
        # Implement your search logic here to find the relevant service
        # For example, you can use Django's queryset filter to search for services
        # Assuming you have a Service model with a 'name' field
        service = Service.objects.filter(service_name__icontains=query).first()
        if service:
            # Generate the URL for the service detail page
            service_detail_url = reverse('service_detail', args=[service.id])
            # Redirect the user to the service detail page
            return redirect(service_detail_url)
        else:
            # If no service is found, you can handle it accordingly (e.g., show a message)
            pass
    return redirect('index')  # Redirect to the home page if no query or no service found

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            # Check if another appointment already exists at the selected date and time
            existing_appointment = Appointment.objects.filter(
                service_date=appointment.service_date,
                service_time=appointment.service_time
            ).exclude(pk=appointment.pk).first()  # Exclude the current appointment if editing
            
            if existing_appointment:
                messages.error(request, 'Another appointment already exists at this date and time.')
                return redirect('book_appointment')
            
            # Assign the currently logged-in user to the user_name field
            appointment.user_name = request.user
            appointment.save()
            
            messages.success(request, 'Appointment booked successfully.')
            return redirect('confirmation')
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form})


def confirmation(request):
    return render(request, 'confirmation.html')


def editprofile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        # Update user profile fields
        if 'profile_pic' in request.FILES:
            user_profile.profile_pic = request.FILES['profile_pic']
        user_profile.address = request.POST.get('address')
        user_profile.phone_no = request.POST.get('phone_no')
        user_profile.state = request.POST.get('state')
        user_profile.country = request.POST.get('country')

        user_profile.save()

        return redirect('viewprofile')

    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'editprofile.html', context)


def addservice(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a success page or service list
            return redirect('service')
    else:
        form = ServiceForm()

    return render(request, 'add-service.html', {'form': form})


def update_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'add-service.html', {'form': form})


def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        service.delete()
        return redirect('service')

    return render(request, 'confdel.html', {'service': service})


def login(request):
    if request.method == "POST":
        username_or_email = request.POST.get('EU')
        password = request.POST.get('pwd')

        user = None
        if '@' in username_or_email:
            # User is trying to log in using email
            user = CustomUser.objects.filter(email=username_or_email).first()
        else:
            # User is trying to log in using username
            user = CustomUser.objects.filter(username=username_or_email).first()

        if user is not None:
            user = authenticate(
                request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)

                if user.role == CustomUser.WORKER:
                    return redirect('workerdashboard')  # Redirect workers to the worker dashboard
                else:
                    return redirect('index')  # Redirect customers to the index page
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')
        else:
            messages.error(request, "User not found.")
            return redirect('login')
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        Cpassword = request.POST.get('cpwd')

        if password == Cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken!")
                return redirect('/signup')

            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken!")
                return redirect('/signup')

            else:
                user_reg = User.objects.create_user(
                    first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user_reg.save()
                user_profile = UserProfile(user=user_reg)
                user_profile.save()
                messages.info(request, "Registered Successfully")
                return redirect('login')
        else:
            return redirect('/signup')
    else:
        return render(request, 'signup.html')

def service_view(request, service_id):
    # Retrieve the service object using the 'service_id' parameter
    service = get_object_or_404(Service, pk=service_id)
    
    # Render the service detail template with the 'service' object
    return render(request, 'service_view.html', {'service': service})

def some_view(request):
    # Your view logic here
    return redirect('ins')  # Redirect to a view named 'ins'


def is_admin(user):
    return user.is_authenticated and user.is_staff


def index(request):
    return render(request, 'index.html')


def service(request):
    return render(request, 'service.html')


def listService(request):
    ser = Service.objects.all()
    return render(request, 'service.html', {'ser': ser})

def viewworker(request):
    workers = Worker.objects.all()  # Fetch all workers from the database
    return render(request, 'worker/viewworker.html', {'workers': workers})

def viewprofile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'viewprofile.html', context)


def base(request):
    return render(request, 'base.html')


def change_password(request):
    return render(request, 'change_password.html')

def workerdashboard(request):
    return render(request, 'worker/workerdashboard.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CustomUser, Worker, UserProfile
from django.core.mail import send_mail

User = get_user_model()

import logging

logger = logging.getLogger(__name__)

@login_required
def addWorker(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            msg = 'Email already exists. Please use a different email address.'
        else:
            # Create a new user
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.is_active = True
            user.role=CustomUser.WORKER
            user.save()

            logger.info(f"User {username} created successfully.")

            # Send welcome email
            send_welcome_email(user.email, password, user.username)

            # Create a Worker instance
            worker = Worker(user=user)
            worker.save()


            # Create a UserProfile
            user_profile = UserProfile(user=user)
            user_profile.save()

            context = {
                 'user': user
    }
            return redirect('workerdashboard')  # Replace 'adminindex' with your desired URL

    # For GET requests or when the form is invalid, render the form
    return render(request, 'addworker.html')


def send_welcome_email(email, password, worker_name):


    login_url = 'http://127.0.0.1:8000/login/'  # Update with your actual login URL
    login_button = f'Click here to log in: {login_url}'


    subject = 'VehiCare Hub - Worker Registration'
    message = f"Hello {worker_name},\n\n"
    message += f"Welcome to VehiCare Hub\n\n"
    message += f"Your registration is complete, and we're excited to have you join us. Here are your login credentials:\n\n"
    message += f"Email: {email}\nPassword: {password}\n\n"
    message += "Please take a moment to log in to your account using the provided credentials. Once you've logged in, we encourage you to reset your password to something more secure and memorable.\n\n"
    message += login_button
    message += "\n\nSoulCure is committed to providing a safe and supportive environment for both therapists and clients. Together, we can make a positive impact on the lives of those seeking healing and guidance.\n"
    message += "Thank you for joining the VehiCare Hub community. We look forward to your contributions and the positive energy you'll bring to our platform.\n\n"
    message += "Warm regards,\nThe VehiCare Hub Team\n\n"
    


    from_email='jessojoseph2024@mca.ajce.in'
      # Replace with your actual email
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)


def worker_details(request):
    user = request.user

    try:
        worker_profile = Workerprofile.objects.get(user=user)
    except Workerprofile.DoesNotExist:
        worker_profile = None

    context = {
        'user': user,
        'worker_profile': worker_profile,
    }
    return render(request, 'worker/worker_details.html', context)

def editworker(request):
    user = request.user
    try:
        worker_profile = Workerprofile.objects.get(user=user)
    except Workerprofile.DoesNotExist:
        worker_profile = None

    if request.method == 'POST':
        # Manually extract data from the request
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        specification = request.POST.get('specification')
        profile_pic = request.FILES.get('profile_pic')

        if not worker_profile:
            # Create a new Workerprofile if it doesn't exist
            worker_profile = Workerprofile(user=user)

        # Update the Workerprofile fields
        worker_profile.fullname = fullname
        worker_profile.phone = phone
        worker_profile.specification = specification

        if profile_pic:
            worker_profile.profile_pic = profile_pic

        worker_profile.save()

        return redirect('worker_details')

    context = {
        'user': user,
        'worker_profile': worker_profile,
    }

    return render(request, 'worker/editworker.html', context)