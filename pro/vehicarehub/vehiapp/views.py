from .forms import AppointmentForm
from .forms import ServiceForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from .models import Service, UserProfile
from .models import Service, UserProfile
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from django.urls import reverse
from .models import Service
from django.db.models import Q

User = get_user_model()

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

# @login_required
# def book_appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
            
#             # Set the user associated with the appointment to the currently logged-in user
#             appointment.user_name = request.user
            
#             try:
#                 # Check if another appointment already exists at the selected date and time
#                 existing_appointment = Appointment.objects.get(
#                     service_date=appointment.service_date,
#                     service_time=appointment.service_time
#                 )
#                 if existing_appointment.pk != appointment.pk:
#                     messages.error(request, 'Another appointment already exists at this date and time.')
#                     return redirect('book_appointment')
#             except ObjectDoesNotExist:
#                 # No existing appointment found, proceed with saving
#                 pass

#             appointment.save()
            
#             messages.success(request, 'Appointment booked successfully.')
#             return redirect('confirmation')
#     else:
#         form = AppointmentForm()

#     return render(request, 'book_appointment.html', {'form': form})

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

        return redirect('index')

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
            user = User.objects.filter(email=username_or_email).first()
        else:
            # User is trying to log in using username
            user = User.objects.filter(username=username_or_email).first()

        if user is not None:
            user = authenticate(
                request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)

                return redirect('/')
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


# def appointment_list(request):
#     return render(request, 'appointment_list.html')
