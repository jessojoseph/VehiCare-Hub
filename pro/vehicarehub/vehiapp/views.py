from .forms import AppointmentForm
from .forms import ServiceForm, CategoryForm, PolicyForm, QuestionForm, ContactusForm, CustomerUserForm, CustomerForm, InsuranceApplicationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .models import Service, UserProfile,Worker,Slot,CustomUser,Appointment, Advisor, Category, PolicyRecord, Policy, Question, AccidentClaim, Surveyor, RoadsideAssistanceRequest
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import datetime, time, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

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

@login_required
def search_services(request):
    query = request.GET.get('query')
    print("Query:", query)

    services_data = []

    if query:
        services = Service.objects.filter(
            Q(service_name__icontains=query) | Q(service_cost__icontains=query)
        )

        for service in services:
            service_dict = {
                'id': service.pk,
                'name': service.service_name,
                'cost': service.service_cost,
                'image': service.service_image.url,
            }
            services_data.append(service_dict)

    return JsonResponse({'services': services_data})


from django.db.models import Count
from django.db.models.functions import ExtractDay
from .models import Appointment, Service, Payment  # Import your models
from .models import Appointment, Service, Payment  # Import your models
from .models import Appointment, Service, Payment  # Import your models

# @login_required
# def book_appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             user = request.user
#             service_date = form.cleaned_data['service_date']
            
#             # Check if the user has an active booking (appointment_status='Scheduled')
#             has_active_booking = Appointment.objects.filter(user_name=user, appointment_status='Scheduled').exists()
            
#             if has_active_booking:
#                 # If the user has an active booking, show a warning
#                 return render(request, 'book_appointment.html', {'form': form, 'service_types': Service.objects.all(), 'has_active_booking': True})
            
#             # Check if the user already has a booking for the selected date
#             existing_booking = Appointment.objects.filter(user_name=user, service_date=service_date).exists()
            
#             if existing_booking:
#                 # If the user already has a booking for the selected date, show a warning
#                 return render(request, 'book_appointment.html', {'form': form, 'service_types': Service.objects.all(), 'existing_booking': True})
            
#             # Check if the maximum limit (9 appointments) is reached for the selected date
#             appointments_count = (
#                 Appointment.objects
#                 .filter(service_date=service_date)
#                 .annotate(day=ExtractDay('service_date'))
#                 .values('day')
#                 .annotate(count=Count('id'))
#                 .order_by('day')
#             )
            
#             if not appointments_count:
#                 # No appointments on the selected date, so it's okay to book
#                 appointment = form.save(commit=False)
#                 appointment.user_name = user
#                 appointment.save()
                
#                 # Create a Payment record (assuming you have a Payment model)

#                 # Redirect the user to the pay.html page to collect payment
#                 return redirect('payment', appointment_id=appointment.id)
                
#             else:
#                 # Check if the count for the selected date is less than 9
#                 if appointments_count[0]['count'] < 9:
#                     # If the limit is not reached, book the appointment
#                     appointment = form.save(commit=False)
#                     appointment.user_name = user
#                     appointment.save()

#                     # Redirect the user to the pay.html page to collect payment
#                     return redirect('pay', appointment_id=appointment.id)
#                 else:
#                     # If the limit is reached, show a warning
#                     return render(request, 'book_appointment.html', {'form': form, 'service_types': Service.objects.all(), 'appointment_limit_reached': True})
#     else:
#         form = AppointmentForm()

#     # Get service types from the Service model
#     service_types = Service.objects.all()

#     context = {
#         'form': form,
#         'service_types': service_types,
#     }

#     return render(request, 'book_appointment.html', context)


from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from django.db.models import Count
from django.db.models.functions import ExtractDay
@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            user = request.user
            service_date = form.cleaned_data['service_date']

            # Check if the user has an active booking (appointment_status='Scheduled')
            has_active_booking = Appointment.objects.filter(user_name=user, appointment_status='Scheduled').exists()

            if has_active_booking:
                # If the user has an active booking, trigger the modal
                return render(request, 'book_appointment.html', {'form': form, 'service_types': Service.objects.all(), 'has_active_booking': True})

            # Check if the user already has a booking for the selected date
            existing_booking = Appointment.objects.filter(user_name=user, service_date=service_date).exists()

            if existing_booking:
                # If the user already has a booking for the selected date, show a warning
                return render(request, 'book_appointment.html', {'form': form, 'service_types': Service.objects.all(), 'existing_booking': True})

            # Check if the maximum limit (9 appointments) is reached for the selected date
            appointments_count = (
                Appointment.objects
                .filter(service_date=service_date)
                .annotate(day=ExtractDay('service_date'))
                .values('day')
                .annotate(count=Count('id'))
                .order_by('day')
            )

            if not appointments_count:
                # No appointments on the selected date, so it's okay to book
                appointment = form.save(commit=False)
                appointment.user_name = user
                appointment.appointment_status = 'Pending'  # Set the appointment status as 'Pending'
                appointment.save()

                # Send a confirmation email to the user
                send_appointment_confirmation_email(user.email, appointment)

                # Create a Payment record (assuming you have a Payment model)
                # Note: Payment status handling should be in your payment handling view

                # Redirect the user to the pay.html page to collect payment
                return redirect('payment', appointment_id=appointment.id)

            else:
                # Check if the count for the selected date is less than 9
                if appointments_count[0]['count'] < 9:
                    # If the limit is not reached, book the appointment
                    appointment = form.save(commit=False)
                    appointment.user_name = user
                    appointment.appointment_status = 'Pending'  # Set the appointment status as 'Pending'
                    appointment.save()

                    # Send a confirmation email to the user
                    send_appointment_confirmation_email(user.email, appointment)

                    # Create a Payment record (assuming you have a Payment model)
                    # Note: Payment status handling should be in your payment handling view

                    # Redirect the user to the pay.html page to collect payment
                    return redirect('payment', appointment_id=appointment.id)
                else:
                    # If the limit is reached, show a warning
                    error_message = 'Appointment limit for the selected date is reached.'
                    return render(request, 'book_appointment.html', {'form': form, 'service_types': Service.objects.all(), 'error_message': error_message})
    else:
        form = AppointmentForm()

    # Get service types from the Service model
    service_types = Service.objects.all()

    context = {
        'form': form,
        'service_types': service_types,
    }

    return render(request, 'book_appointment.html', context)

def send_appointment_confirmation_email(email, appointment):
    subject = 'Appointment Confirmation'
    message = f"Hello,\n\n"
    message += f"Welcome to VehiCare Hub\n\n"
    message = f'Your appointment for the vehicle {appointment.registration_number} on {appointment.service_date} has been successfully scheduled.'
    message += f'Thank you for choosing our services!\n\n'
    message += f'Best regards,\nThe VehiCare Hub Team'
    from_email = 'jessojoseph2024@mca.ajce.in'  # Replace with your email
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


@login_required
def viewappointment(request):
    if request.user.is_staff:
        # Admin user can view all appointments, sorted by service_date (ascending)
        appointments = Appointment.objects.all().order_by('service_date')
    else:
        # Regular user can only view their own appointments, sorted by service_date (ascending)
        appointments = Appointment.objects.filter(user_name=request.user).order_by('service_date')
    
    context = {'appointments': appointments}
    return render(request, 'viewappointments.html', context)

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    print(appointment_id)

    if request.method == 'POST':
        # Perform the cancellation logic here (e.g., change status to 'Cancelled')
        appointment.appointment_status = 'Cancelled'
        appointment.save()

        appointment.delete()

        return redirect('viewappointments')
    return render(request, 'viewappointments.html', {'appointment': appointment})


from datetime import datetime, timedelta, time, date

def create_daily_slots(request):
    if request.method == 'GET':
        # Check if the slots for today already exist
        if not Slot.objects.filter(service_date=date.today()).exists():
            start_time = time(9, 0)  # Start at 9:00 AM
            end_time = time(17, 0)   # End at 5:00 PM
            slot_duration = timedelta(minutes=90)

            current_time = datetime.combine(date.today(), start_time)
            end_datetime = datetime.combine(date.today(), end_time)

            while current_time < end_datetime:
                slot = Slot(service_time=current_time.time(), is_booked=False)
                slot.save()
                current_time += slot_duration

        return HttpResponse("Daily slots have been created.")
    else:
        return HttpResponse("Invalid request method.")

def confirmation(request):
    return render(request, 'confirmation.html')

from django.contrib.auth.decorators import login_required
from django.http import Http404

@login_required
def editprofile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # Handle the case when the user profile does not exist
        raise Http404("User profile not found")

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

        # Check if the user exists by username or email
        user = None
        if '@' in username_or_email:
            user = CustomUser.objects.filter(email=username_or_email).first()
        else:
            user = CustomUser.objects.filter(username=username_or_email).first()

        if user is not None:
            # Check if the provided password is correct
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)

                # Redirect based on user role
                if user.role == CustomUser.WORKER:
                    return redirect('workerdashboard')  # Redirect workers to the worker dashboard
                elif user.role == CustomUser.ADVISOR:
                    return redirect('insureadmindash')  # Redirect advisors to the insure1 page
                elif user.role == CustomUser.SURVEYOR:
                    return redirect('survayordashboard')  # Redirect surveyors to the surveyordashboard page
                else:
                    return redirect('index')  # Redirect other roles to the index page
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

def admindash(request):
    return render(request, 'admindash.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CustomUser, Worker, UserProfile
from django.core.mail import send_mail

User = get_user_model()

import logging

logger = logging.getLogger(__name__)
def addWorker(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email address.')
        else:
            # Create a new user
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.is_active = True
            user.role = CustomUser.WORKER
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

            messages.success(request, 'Worker created successfully.')
            return redirect('addworker')  # Replace 'addworker' with your desired URL

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
    user =    user = request.user
    userid = request.user.id

    try:
        now_worker=CustomUser.objects.get(id=userid)
        worker_profile = UserProfile.objects.get(user=user)
        worker = Worker.objects.get(user=user)
    except UserProfile.DoesNotExist:
        worker_profile = None

    context = {
        'user': user,
        'now_worker': now_worker,
        'worker_profile': worker_profile,
        'worker':worker,
    }
    return render(request, 'worker/worker_details.html', context)

def editworker(request):
    user = request.user
    userid = request.user.id

    try:
        now_worker=CustomUser.objects.get(id=userid)
        worker_profile = UserProfile.objects.get(user=user)
        worker = Worker.objects.get(user=user)
    except UserProfile.DoesNotExist:
        worker_profile = None
        worker=None

    if request.method == 'POST':
        # Manually extract data from the request
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        specification = request.POST.get('specification')
        profile_pic = request.FILES.get('profile_pic')
        experience = request.POST.get('experience')


        print(fname,lname)

        # Update the Workerprofile fields
        user.first_name = fname
        user.last_name = lname
        worker_profile.phone_no = phone
        worker.specialized_service = specification
        worker.experience = experience


        if profile_pic:
            worker_profile.profile_pic = profile_pic

        worker_profile.save()
        worker.save()
        user.save()

        return redirect('worker_details')

    context = {
        'user': user,
        'worker_profile': worker_profile,
       'worker':worker,
    }

    return render(request, 'worker/editworker.html', context)
def view_service(request,view_id):
    ser=Service.objects.get(id=view_id)
    print(ser)
    return render(request,'viewservice.html',{'ser':ser})

def task(request):
    return render(request, 'worker/task.html')




from django.shortcuts import render, redirect, get_object_or_404
from .models import Worker, Appointment, Task

def assign_task(request):
    if request.method == 'POST':
        worker_id = request.POST.get('worker_id')
        appointment_id = request.POST.get('appointment_id')
        
        if worker_id and appointment_id:
            try:
                worker = Worker.objects.get(id=worker_id)
                appointment = Appointment.objects.get(id=appointment_id)
                
                if worker.is_available:
                    task = Task.objects.create(
                        title=f"Task for {appointment.user_name.username}",
                        description=f"Assignment for appointment on {appointment.service_date} at {appointment.service_time}",
                        worker=worker,
                        appointment=appointment,  # Assign the selected appointment to the task
                        status='pending',  # Set the initial status as pending or as needed
                        deadline=appointment.service_date,  # Set the deadline based on the appointment date
                    )
                    
                    # Mark the worker as unavailable after assigning the task
                    worker.is_available = False
                    worker.save()
                    
                    # Update the appointment status if needed
                    appointment.appointment_status = 'Assigned'
                    appointment.save()
                    
                    return redirect('viewappointments')  # Redirect to a task list page or other appropriate page
                else:
                    # Handle the case when the worker is not available
                    # You can display a message or redirect to an error page
                    pass  # Add your code here
                
            except Worker.DoesNotExist:
                # Handle the case when no matching worker is found
                pass  # Add your code here
                
            except Appointment.DoesNotExist:
                # Handle the case when no matching appointment is found
                pass  # Add your code here

    # Render the task assignment form
    workers = Worker.objects.filter(is_available=True)  # Fetch available workers
    appointments = Appointment.objects.filter(appointment_status='Scheduled')  # Fetch scheduled appointments
    return render(request, 'assign_task.html', {'workers': workers, 'appointments': appointments})


from django.shortcuts import render
from .models import Task, Worker
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from .models import Task, AudioRecording  # Import the AudioRecording model

@login_required
def worker_dashboard_tasks(request):
    try:
        worker = Worker.objects.get(user=request.user)
        worker_tasks = Task.objects.filter(worker=worker)
    except Worker.DoesNotExist:
        worker_tasks = []  # Handle the case where the logged-in user is not a worker

    context = {'worker_tasks': worker_tasks}
    return render(request, 'worker/task.html', context)


@login_required
def work_overview(request):
    try:
        # Get the logged-in user
        user = request.user

        # Check if the user is a worker
        try:
            worker = Worker.objects.get(user=user)
        except Worker.DoesNotExist:
            worker = None

        if worker:
            # User is a worker, get counts and tasks for the worker
            completed_tasks_count = Task.objects.filter(worker=worker, status='completed').count()
            assigned_tasks_count = Task.objects.filter(worker=worker, status__in=['in_progress', 'pending']).count()
            completed_tasks = Task.objects.filter(worker=worker, status='completed')
            assigned_tasks = Task.objects.filter(worker=worker, status__in=['in_progress', 'pending'])
        else:
            # User is not a worker, initialize counts and tasks as empty
            completed_tasks_count = 0
            assigned_tasks_count = 0
            completed_tasks = []
            assigned_tasks = []

        context = {
            'completed_tasks_count': completed_tasks_count,
            'assigned_tasks_count': assigned_tasks_count,
            'completed_tasks': completed_tasks,
            'assigned_tasks': assigned_tasks,
        }
        return render(request, 'worker/work_overview.html', context)
    except CustomUser.DoesNotExist:
        # Handle the case where the logged-in user does not exist
        return render(request, 'worker/work_overview.html', {})


from .models import LeaveRequest  # Import your LeaveRequest model
from django.contrib import messages

@login_required
def leave_request(request):
    try:
        # Get the logged-in user
        user = request.user

        # Check if the user is associated with a Worker
        try:
            worker = Worker.objects.get(user=user)
        except Worker.DoesNotExist:
            worker = None

        if worker:
            if request.method == 'POST':
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                reason = request.POST['reason']
                
                # Create a LeaveRequest object and save it to the database
                leave_request = LeaveRequest(
                    worker=worker,
                    start_date=start_date,
                    end_date=end_date,
                    reason=reason,
                    status='pending'  # Set the default status here if needed
                )
                leave_request.save()

                # Optionally, you can display a success message
                messages.success(request, 'Leave request submitted successfully.')

                return redirect('workerdashboard')  # Redirect to the worker dashboard or another appropriate page

            return render(request, 'worker/leave_request.html')
        else:
            # Handle the case where the logged-in user is not associated with a Worker
            messages.error(request, 'You must be a worker to apply for leave.')
            return redirect('workerdashboard')  # Redirect to an appropriate page

    except CustomUser.DoesNotExist:
        # Handle the case where the logged-in user does not exist
        return render(request, 'worker/leave_request.html', {})
    

def view_leavereq(request):
    if request.method == 'POST':
        # Handle the form submission for approving or rejecting leave requests
        leave_request_id = request.POST.get('leave_request_id')
        action = request.POST.get('action')  # 'approve' or 'reject'

        try:
            leave_request = LeaveRequest.objects.get(id=leave_request_id)
            if action == 'approve':
                leave_request.status = 'approved'
            elif action == 'reject':
                leave_request.status = 'rejected'
            leave_request.save()

            # Debug output to check if the view is being called
            print(f"AJAX request received: {action} leave request {leave_request_id}")
            
            # Return a JSON response indicating success
            return JsonResponse({'success': True})

        except LeaveRequest.DoesNotExist:
            # Handle if the leave request doesn't exist
            pass

    # Retrieve all leave requests for display
    leave_requests = LeaveRequest.objects.all()

    # Prepare a list of statuses for use in the template
    statuses = ['approved', 'rejected']

    context = {
        'leave_requests': leave_requests,
        'statuses': statuses,
    }
    return render(request, 'view_leavereq.html', context)


def view_leavestat(request):
    if request.user.is_authenticated:

        worker = request.user  # Assuming this is the currently logged-in user
        current_worker = Worker.objects.get(user=worker)  # Assuming you want to get the worker based on the user

        leave_requests = LeaveRequest.objects.filter(worker=current_worker)
        print(leave_requests)


        context = {
            'leave_requests': leave_requests,
            'current_worker': current_worker,  # Pass the current worker to the template
        }

        return render(request, 'worker/view_leavestat.html', context)
    else:
        return render(request, 'worker/view_leavestat.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Worker, Appointment

# def update_work_status(request, task_id):
#     task = get_object_or_404(Task, id=task_id)

#     if request.method == 'POST':
#         new_status = request.POST.get('new_status')
#         work_done = request.POST.get('work_done')
#         materials_used = request.POST.get('materials_used')
#         additional_notes = request.POST.get('additional_notes')
#         audio_data = request.FILES.get('audio_data')

#         task.status = new_status
#         task.work_done = work_done
#         task.materials_used = materials_used
#         task.additional_notes = additional_notes

#         # Check if audio_data is provided and save it to the database
#         if audio_data:
#             task.audio_file.save(audio_data.name, audio_data)

#         task.save()

#         # Check if the task is marked as completed
#         if new_status == 'completed':
#             # Get the worker associated with the task
#             worker = task.worker

#             # Mark the worker as available for other jobs
#             worker.is_available = True
#             worker.save()

#              # Update the appointment status associated with this task
#             appointment = task.appointment
#             appointment.appointment_status = 'Completed'
#             appointment.save()

#         return redirect('workerdashboard')

#     return render(request, 'worker/update_work_status.html', {'task': task})


def update_work_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        work_done = request.POST.get('work_done')
        materials_used = request.POST.get('materials_used')
        additional_notes = request.POST.get('additional_notes')
        audio_data = request.FILES.get('audio_data')
        recognized_text = request.POST.get('recognized_text')  # Extract recognized text

        task.status = new_status
        task.work_done = work_done
        task.materials_used = materials_used
        task.additional_notes = additional_notes
        task.recognized_text = recognized_text  # Save recognized text to the recognized_text field

        # Check if audio_data is provided and save it to the database
        if audio_data:
            task.audio_file.save(audio_data.name, audio_data)

            # Here, you might want to add a call to a function to process the audio
            process_audio(task, audio_data)

        task.save()

        # Check if the task is marked as completed
        if new_status == 'completed':
            # Get the worker associated with the task
            worker = task.worker

            # Mark the worker as available for other jobs
            worker.is_available = True
            worker.save()

            # Update the appointment status associated with this task
            appointment = task.appointment
            appointment.appointment_status = 'Completed'    
            appointment.save()

        # return JsonResponse({'message': 'Work status updated successfully'})

    return render(request, 'worker/update_work_status.html', {'task': task})


def process_audio(task, audio_data):
    # Implement logic to process the audio if needed
    # For example, you can transcribe the audio, analyze it, etc.
    pass

from .models import Task, CustomUser, Appointment
@login_required
def view_updates(request):
    user = request.user

    completed_tasks = Task.objects.filter(status='completed', appointment__user_name=user)
    ongoing_tasks = Task.objects.filter(status='in_progress', appointment__user_name=user)
    user_appointments = Appointment.objects.filter(user_name=user)

    context = {
        'completed_tasks': completed_tasks,
        'ongoing_tasks': ongoing_tasks,
        'user_appointments': user_appointments,
    }
    
    return render(request, 'view_updates.html', context)

@login_required
def admin_view_updates(request):
    if request.user.is_superuser:
        # Filter users with the customer role
        customers = User.objects.filter(role=CustomUser.CUSTOMER)
        
        # Print all customer usernames to the terminal
        for customer in customers:
            print(f"Customer: {customer.username}")
        
        selected_user_id = request.GET.get('selected_user', None)
        selected_user = None
        tasks = []

        if selected_user_id:
            selected_user = User.objects.get(pk=selected_user_id)
            # Retrieve tasks for the selected user
            tasks = Task.objects.filter(appointment__user_name=selected_user)

        context = {
            'customers': customers,  # Pass the list of customers to the template
            'selected_user': selected_user,
            'tasks': tasks,
        }

        return render(request, 'admin_view_updates.html', context)
    else:
        # Handle non-admin users here
        return render(request, 'access_denied.html')



# View for handling payment callbacks
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.conf import settings
from .models import Payment, Appointment  # Import your models
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core import signing
import hmac, hashlib



# Initialize the Razorpay client
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)


# View for initiating a payment
def payment(request, appointment_id):
    # Retrieve the current appointment
    current_appointment = get_object_or_404(Appointment, pk=appointment_id)

    # For Razorpay integration
    currency = 'INR'
    amount = 150  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('paymenthandler', args=[appointment_id])  # Define your callback URL here

    # Create a Payment record
    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        payment_id="",  # You can update this later
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        appointment=current_appointment
    )
    payment.save()

    # Prepare the context data
    context = {
        'user': request.user,
        'appointment': current_appointment,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
    }

    return render(request, 'pay.html', context)

@csrf_exempt
def paymenthandler(request, appointment_id):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        # Verify the payment signature using Razorpay's verify_payment_signature function
        result = razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        
        # Payment signature is valid
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        amount = int(payment.amount * 100)  # Convert Decimal to paise

        # Capture the payment
        razorpay_client.payment.capture(payment_id, amount)

        # Update the payment status
        payment.payment_id = payment_id
        payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
        payment.save()

        # Update the appointment status to 'Scheduled'
        update_appointment = Appointment.objects.get(id=appointment_id)
        update_appointment.appointment_status = 'Scheduled'  # Update the status field
        update_appointment.save()

        # Redirect to the confirmation page upon successful payment
        return render(request, 'confirmation.html', {'appointment': update_appointment})

    return HttpResponseBadRequest()

import pandas as pd
import joblib
from .models import ServiceTimePrediction  # Import the model(s) you created
from django.http import JsonResponse  # Import JsonResponse

def prediction(request):
    if request.method == 'POST':
        # Get user inputs from the HTML form
        bike_model = request.POST['bike_model']
        bike_age = int(request.POST['bike_age'])
        service_type = request.POST['service_type']
        service_history = int(request.POST['service_history'])
        build_year = int(request.POST['build_year'])
        mileage = int(request.POST['mileage'])
        last_serviced_date = int(request.POST['last_serviced_date'])
        current_year = int(request.POST['current_year'])

        # Load the trained model and label encoders
        model = joblib.load('models/rf_model.pkl')  # Correct the path
        label_encoders = joblib.load('models/label_encoders.pkl')  # Correct the path

        # Create a DataFrame for the user input
        user_data = pd.DataFrame({
            'Bike_Model': [bike_model],
            'Age': [bike_age],
            'Service_Type': [service_type],
            'Service_History': [service_history],
            'Build_Year': [build_year],
            'Mileage (km)': [mileage],
            'Last_Serviced_Date (months)': [last_serviced_date],
            'Current_Year': [current_year]
        })

        # Encode categorical variables in the user data
        for column in ['Bike_Model', 'Service_Type']:
            user_data[column] = label_encoders[column].transform(user_data[column])

        # Make predictions for the user input
        predicted_hours = model.predict(user_data)

        # Predicted hours and minutes
        predicted_hours = int(predicted_hours[0])
        predicted_minutes = int(predicted_hours % 60)

        # Prepare the data to return in JSON format
        response_data = {
            'predicted_hours': predicted_hours,
            'predicted_minutes': predicted_minutes,
        }

        # Return a JSON response
        return JsonResponse(response_data)

    # Render the initial form
    return render(request, 'worker/checkcondition.html')




def login2(request):
    return render(request, 'login2.html')

def insureadmindash(request):
    return render(request, 'insurance/insureadmindash.html')

logger = logging.getLogger(__name__)
def addadvisor(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email address.')
        else:
            # Create a new user
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.is_active = True
            user.role = CustomUser.ADVISOR
            user.save()

            logger.info(f"User {username} created successfully.")

            # Send welcome email
            send_welcome_emails(user.email, password, user.username)

            # Create a Worker instance
            advisor = Advisor(user=user)
            advisor.save()

            # Create a UserProfile
            user_profile = UserProfile(user=user)
            user_profile.save()

            messages.success(request, 'New advisor created successfully.')
            return redirect('addadvisor')  # Replace 'addworker' with your desired URL

    # For GET requests or when the form is invalid, render the form
    return render(request, 'insurance/addadvisor.html')

def send_welcome_emails(email, password, worker_name):


    login_url = 'http://127.0.0.1:8000/login/'  # Update with your actual login URL
    login_button = f'Click here to log in: {login_url}'


    subject = 'VehiCare Hub - Insurance Advisor Registration'
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
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
def admin_policy_view(request):
    return render(request,'insurance/admin_policy.html')




def admin_category_view(request):
    return render(request,'insurance/admin_category.html')

def admin_add_category_view(request):
    categoryForm=CategoryForm() 
    if request.method=='POST':
        categoryForm=CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin_view_category')
    return render(request,'insurance/admin_add_category.html',{'categoryForm':categoryForm})

def admin_view_category_view(request):
    categories = Category.objects.all()
    return render(request,'insurance/admin_view_category.html',{'categories':categories})

def admin_delete_category_view(request):
    categories = Category.objects.all()
    return render(request,'insurance/admin_delete_category.html',{'categories':categories})
    
def delete_category_view(request,pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('admin_delete_category')

def admin_update_category_view(request):
    categories = Category.objects.all()
    return render(request,'insurance/admin_update_category.html',{'categories':categories})

def update_category_view(request,pk):
    category = Category.objects.get(id=pk)
    categoryForm=CategoryForm(instance=category)
    
    if request.method=='POST':
        categoryForm=CategoryForm(request.POST,instance=category)
        
        if categoryForm.is_valid():

            categoryForm.save()
            return redirect('admin_update_category')
    return render(request,'insurance/update_category.html',{'categoryForm':categoryForm})
  
    

def admin_policy_view(request):
    return render(request,'insurance/admin_policy.html')


def admin_add_policy_view(request):
    policyForm=PolicyForm() 
    
    if request.method=='POST':
        policyForm=PolicyForm(request.POST)
        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
            return redirect('admin_view_policy')
    return render(request,'insurance/admin_add_policy.html',{'policyForm':policyForm})

def admin_view_policy_view(request):
    policies = Policy.objects.all()
    return render(request,'insurance/admin_view_policy.html',{'policies':policies})

def admin_update_policy_view(request):
    policies = Policy.objects.all()
    return render(request,'insurance/admin_update_policy.html',{'policies':policies})

def update_policy_view(request,pk):
    policy = Policy.objects.get(id=pk)
    policyForm=PolicyForm(instance=policy)
    
    if request.method=='POST':
        policyForm=PolicyForm(request.POST,instance=policy)
        
        if policyForm.is_valid():

            categoryid = request.POST.get('category')
            category = Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
           
            return redirect('admin_update_policy')
    return render(request,'insurance/update_policy.html',{'policyForm':policyForm})
  
  
def admin_delete_policy_view(request):
    policies = Policy.objects.all()
    return render(request,'insurance/admin_delete_policy.html',{'policies':policies})
    
def delete_policy_view(request,pk):
    policy = Policy.objects.get(id=pk)
    policy.delete()
    return redirect('admin_delete_policy')

def admin_view_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all()
    return render(request,'insurance/admin_view_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_approved_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all().filter(status='Approved')
    return render(request,'insurance/admin_view_approved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_disapproved_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all().filter(status='Disapproved')
    return render(request,'insurance/admin_view_disapproved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_waiting_policy_holder_view(request):
    policyrecords = PolicyRecord.objects.all().filter(status='Pending')
    return render(request,'insurance/admin_view_waiting_policy_holder.html',{'policyrecords':policyrecords})

def approve_request_view(request,pk):
    policyrecords = PolicyRecord.objects.get(id=pk)
    policyrecords.status='Approved'
    policyrecords.save()
    return redirect('admin_view_policy_holder')

def disapprove_request_view(request,pk):
    policyrecords = PolicyRecord.objects.get(id=pk)
    policyrecords.status='Disapproved'
    policyrecords.save()
    return redirect('admin_view_policy_holder')


def admin_question_view(request):
    questions = Question.objects.all()
    return render(request,'insurance/admin_question.html',{'questions':questions})

def update_question_view(request,pk):
    question = Question.objects.get(id=pk)
    questionForm=QuestionForm(instance=question)
    
    if request.method=='POST':
        questionForm=QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            admin_comment = request.POST.get('admin_comment')
            
            
            question = questionForm.save(commit=False)
            question.admin_comment=admin_comment
            question.save()
           
            return redirect('admin_question')
    return render(request,'insurance/update_question.html',{'questionForm':questionForm})

def aboutus_view(request):
    return render(request,'insurance/aboutus.html')

def contactus_view(request):
    sub = ContactusForm()
    if request.method == 'POST':
        sub = ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'insurance/contactussuccess.html')
    return render(request, 'insurance/contactus.html', {'form':sub})

def admin_view_customer_view(request):
    customers= CustomUser.objects.filter(role=2)
    return render(request,'insurance/admin_view_customer.html',{'customers':customers})

from .forms import CustomerUserForm, CustomerForm

def update_customer_view(request, pk):
    customer = CustomUser.objects.get(id=pk)
    user_profile = UserProfile.objects.get(user=customer)

    userForm = CustomerUserForm(instance=customer)
    customerForm = CustomerForm(instance=user_profile)

    mydict = {'userForm': userForm, 'customerForm': customerForm}

    if request.method == 'POST':
        userForm = CustomerUserForm(request.POST, instance=customer)
        customerForm = CustomerForm(request.POST, request.FILES, instance=user_profile)

        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer_profile = customerForm.save(commit=False)
            customer_profile.user = user
            customer_profile.save()
            return redirect('admin_view_customer')

    return render(request, 'insurance/update_customer.html', context=mydict)

def delete_customer_view(request,pk):
    customer=CustomUser.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return render('/admin_view_customer')

def insureadmindash(request):
    dict={
        'total_user':CustomUser.objects.filter(role=2).count(),
        'total_policy':Policy.objects.all().count(),
        'total_category':Category.objects.all().count(),
        'total_question':Question.objects.all().count(),
        'total_policy_holder':PolicyRecord.objects.all().count(),
        'approved_policy_holder':PolicyRecord.objects.all().filter(status='Approved').count(),
        'disapproved_policy_holder':PolicyRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_policy_holder':PolicyRecord.objects.all().filter(status='Pending').count(),
        'total_survayor':CustomUser.objects.filter(role=4).count(),

    }
    return render(request,'insurance/insureadmindash.html',context=dict)





def customer_dashboard_view(request):
    dict={
        'customer':CustomUser.objects.get(id=request.user.id),
        'available_policy':Policy.objects.all().count(),
        'applied_policy':PolicyRecord.objects.all().filter(customer=CustomUser.objects.get(id=request.user.id)).count(),
        'total_category':Category.objects.all().count(),
        'total_question':Question.objects.all().filter(customer=CustomUser.objects.get(id=request.user.id)).count(),
        'total_claims':AccidentClaim.objects.all().count(),

    }
    return render(request,'insurance/customer_dashboard.html',context=dict)

def apply_policy_view(request):
    customer = CustomUser.objects.get(id=request.user.id)
    policies = Policy.objects.all()
    return render(request,'insurance/apply_policy.html',{'policies':policies,'customer':customer})

def apply_view(request,pk):
    customer = CustomUser.objects.get(id=request.user.id)
    policy = Policy.objects.get(id=pk)
    policyrecord = PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('history')

def history_view(request):
    customer = CustomUser.objects.get(id=request.user.id)
    policies = PolicyRecord.objects.all().filter(customer=customer)
    return render(request,'insurance/history.html',{'policies':policies,'customer':customer})

def ask_question_view(request):
    customer = CustomUser.objects.get(id=request.user.id)
    questionForm=QuestionForm() 
    
    if request.method=='POST':
        questionForm=QuestionForm(request.POST)
        if questionForm.is_valid():
            
            question = questionForm.save(commit=False)
            question.customer=customer
            question.save()
            return redirect('question_history')
    return render(request,'insurance/ask_question.html',{'questionForm':questionForm,'customer':customer})

def question_history_view(request):
    customer = CustomUser.objects.get(id=request.user.id)
    questions = Question.objects.all().filter(customer=customer)
    return render(request,'insurance/question_history.html',{'questions':questions,'customer':customer})

from decimal import Decimal

def apply_insurance_view(request, pk):
    policy = get_object_or_404(Policy, id=pk)

    if request.method == 'POST':
        form = InsuranceApplicationForm(request.POST)
        if form.is_valid():
            # Process the form data and save the insurance application record
            application_record = PolicyRecord()
            application_record.Policy = policy
            application_record.customer = request.user
            application_record.vehicle_number = form.cleaned_data['vehicle_number']
            application_record.purchase_year = form.cleaned_data['purchase_year']
            application_record.full_name = form.cleaned_data['full_name']
            application_record.mob_number = form.cleaned_data['mob_number']
            application_record.rc_number = form.cleaned_data['rc_number']
            application_record.chassis_number = form.cleaned_data['chassis_number']

            # Additional fields for premium calculation
            application_record.bike_model = form.cleaned_data['bike_model']
            application_record.bike_make = form.cleaned_data['bike_make']
            application_record.engine_capacity = form.cleaned_data['engine_capacity']
            application_record.owner_age = form.cleaned_data['owner_age']
            application_record.owner_gender = form.cleaned_data['owner_gender']
            application_record.riding_experience = form.cleaned_data['riding_experience']
            application_record.voluntary_deductible = form.cleaned_data['voluntary_deductible']
            application_record.has_previous_claim = form.cleaned_data['has_previous_claim']
            application_record.add_ons = form.cleaned_data['add_ons']

            # Calculate premium based on factors (example calculation)
            base_premium = Decimal('2000')  # Adjust this based on your requirements
            age_factor = Decimal('1.0') if application_record.owner_age < 25 else Decimal('0.9')
            experience_factor = Decimal('1.0') if application_record.riding_experience > 3 else Decimal('1.2')
            premium = base_premium * age_factor * experience_factor

            # Update the premium field in the model
            application_record.premium = premium
            application_record.save()

            return redirect('history') 
    else:
        form = InsuranceApplicationForm()

    return render(request, 'insurance/apply_insurance.html', {'form': form, 'policy': policy})


def submit_claim_view(request):
    if request.method == 'POST':
        incident_type = request.POST.get('incident_type')
        incident_date = request.POST.get('incident_date')
        description = request.POST.get('description')
        fir_document = request.FILES.get('fir_document')
        dl_document = request.FILES.get('dl_document')
        rc_document = request.FILES.get('rc_document')

        user = request.user
        accident_claim = AccidentClaim(
            user=user,
            incident_type=incident_type,
            incident_date=incident_date,
            description=description,
            fir_document=fir_document,
            dl_document=dl_document,
            rc_document=rc_document
        )
        accident_claim.save()

        print("Claim submitted successfully!")
        return HttpResponse("Claim submitted successfully!")
    else:
        return render(request, 'insurance/submit_claim.html')


def history_claim_view(request):
    accident_claims = AccidentClaim.objects.filter(user=request.user)

    context = {
        'accident_claims': accident_claims,
    }
    return render(request, 'insurance/history_claim.html', context)


def admin_history_claim_view(request):
    accident_claims = AccidentClaim.objects.all()

    context = {
        'accident_claims': accident_claims,
    }
    return render(request, 'insurance/admin_history_claim.html', context)

def admin_history_claim_view(request):
    accident_claims = AccidentClaim.objects.all()

    context = {
        'accident_claims': accident_claims,
    }
    return render(request, 'insurance/admin_history_claim.html', context)

def approve_claim(request, claim_id):
    accident_claim = get_object_or_404(AccidentClaim, id=claim_id)

    if accident_claim.status == 'Pending':
        accident_claim.status = 'Approved'
        accident_claim.save()

    return redirect('admin_history_claim')

def reject_claim(request, claim_id):
    accident_claim = get_object_or_404(AccidentClaim, id=claim_id)

    if accident_claim.status == 'Pending':
        accident_claim.status = 'Rejected'
        
        rejection_reason = request.POST.get('rejection_reason')
        accident_claim.rejection_reason = rejection_reason

        accident_claim.save()

    return redirect('admin_history_claim')

logger = logging.getLogger(__name__)

def register_surveyor(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email address.')
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.is_active = True
            user.role = CustomUser.SURVEYOR
            user.save()

            logger.info(f"User {username} created successfully.")

            surveyor = Surveyor(user=user, name=username)
            surveyor.save()

            user_profile = UserProfile(user=user)
            user_profile.save()

            messages.success(request, 'New surveyor created successfully.')
            return redirect('admin_add_surveyor')

    return render(request, 'insurance/admin_add_surveyor.html')


def survayor_dashboard(request):
    user = request.user
    userProfile = UserProfile.objects.filter(user=user)
    context = {
        'userProfile' : userProfile,
    } 

    return render(request,'insurance/survayordashboard.html', context)

def survayor_base_dashboard(request):
    return render(request,'insurance/survayorbase.html')

def update_survayor_view(request, pk):
    # Assuming pk is the primary key of the surveyor you want to update
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if not user.is_authenticated:
        # Redirect to login or handle the case where the user is not authenticated
        return redirect('login')

    # Assuming you want to get the surveyor based on the given primary key
    surveyor = get_object_or_404(CustomUser, pk=pk)

    # Assuming you have a UserProfile associated with the surveyor
    profile = get_object_or_404(UserProfile, user=user)

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

        messages.success(request, 'Surveyor updated successfully!')
        return redirect('update_survayor', pk=pk)  # Redirect to the appropriate page
    context = {
        'user': user,
        'user_profile': user_profile
    }
    return render(request, 'insurance/update_survayor.html', context)

def admin_view_survayor_view(request):
    surveyors = CustomUser.objects.filter(role=CustomUser.SURVEYOR, is_active=True)
    return render(request, 'insurance/admin_view_survayor.html', {'surveyors': surveyors})

def assign_claim_view(request):
    if request.method == 'POST':
        selected_claim_ids = request.POST.getlist('claims[]')
        surveyor_id = request.POST.get('surveyor')

        if not surveyor_id:
            messages.error(request, 'Please select a surveyor.')
            return redirect('admin_assign_claim')

        selected_claims = AccidentClaim.objects.filter(id__in=selected_claim_ids, is_assigned=False)

        for claim in selected_claims:
            claim.is_assigned = True
            claim.assigned_surveyor_id = surveyor_id  # Assign the surveyor
            claim.status = 'Approved'  # Update status as needed
            claim.save()

        messages.success(request, 'Claims assigned successfully.')
        return redirect('admin_assign_claim')

    approved_claims = AccidentClaim.objects.filter(status='Approved', is_assigned=False)

    available_surveyors = Surveyor.objects.filter(is_available=True)
    available_advisors = Advisor.objects.filter(is_available=True)

    context = {
        'approved_claims': approved_claims,
        'available_surveyors': available_surveyors,
        'available_advisors': available_advisors,
    }

    return render(request, 'insurance/admin_assign_claim.html', context)


def surveyor_assigned_claims(request):
    logged_in_surveyor = Surveyor.objects.get(user=request.user)

    assigned_claims = AccidentClaim.objects.filter(assigned_surveyor=logged_in_surveyor, is_assigned=True)

    context = {
        'assigned_claims': assigned_claims,
    }

    return render(request, 'insurance/surveyor_assigned_claims.html', context)


def view_claim_details(request, claim_id):
    claim = get_object_or_404(AccidentClaim, id=claim_id)
    policy_record = PolicyRecord.objects.filter(customer=claim.user).first()
    context = {'claim': claim, 'policyrecord': policy_record}
    return render(request, 'insurance/view_claim_details.html', context)

def request_assistance(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        reg_number = request.POST.get('reg_number')
        complaint = request.POST.get('complaint')
        phone_number = request.POST.get('phone_number')  # New field for phone number
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Create a new RoadsideAssistanceRequest object
        request = RoadsideAssistanceRequest.objects.create(
            name=name,
            reg_number=reg_number,
            complaint=complaint,
            phone_number=phone_number,  # New field for phone number
            latitude=latitude,
            longitude=longitude
        )
        # Redirect to a success page
        return redirect('assistance')
    
    # Get the name of the currently logged-in user
    logged_in_user_name = request.user.username
    
    # Pass the logged-in user's name to the template
    context = {
        'logged_in_user_name': logged_in_user_name
    }
    
    return render(request, 'assistance.html', context)


def breakdown_requests(request):
    breakdown_requests = RoadsideAssistanceRequest.objects.all()
    workers = Worker.objects.filter(is_available=True)  # Retrieve available workers
    context = {
        'breakdown_requests': breakdown_requests,
        'workers': workers,
    }
    return render(request, 'assistance_requests.html', context)

def assign_breakdown(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        worker_id = request.POST.get('worker_id')

        # Retrieve the assistance request and the selected worker
        assistance_request = RoadsideAssistanceRequest.objects.get(id=request_id)
        worker = Worker.objects.get(id=worker_id)

        # Assign the assistance request to the worker
        assistance_request.assigned_worker = worker
        assistance_request.save()

        # Update the worker's availability status
        worker.is_available = False
        worker.save()

        return redirect('assistance_requests') 

    
def worker_breakdown(request):
    # Check if the current user is associated with a Worker
    try:
        # Retrieve the associated Worker for the current user
        worker = Worker.objects.get(user=request.user)
        
        # Retrieve assigned assistance requests for the associated worker
        assigned_requests = RoadsideAssistanceRequest.objects.filter(assigned_worker=worker)
        
        context = {
            'assigned_requests': assigned_requests,
        }
        return render(request, 'worker/worker_breakdown.html', context)
    except Worker.DoesNotExist:
        # Handle the case where the current user is not associated with a Worker
        # You can render an appropriate template or return an empty context
        return render(request, 'worker/worker_breakdown.html', {})
    

import random
from twilio.rest import Client

def send_otp_to_customer(request, request_id):
    # Retrieve the roadside assistance request object
    roadside_request = get_object_or_404(RoadsideAssistanceRequest, id=request_id)
    
    # Generate OTP
    otp = ''.join(random.choices('0123456789', k=6))
    roadside_request.otp = otp
    roadside_request.save()
    
    # Send OTP via SMS
    send_otp_via_sms(roadside_request.phone_number, otp)
    
    return redirect('worker_breakdown')

def send_otp_via_sms(mobile_number, otp):
    # Your Twilio credentials
    account_sid = 'AC17eaba11961da3bd30897bbd2754bbb5'
    auth_token = '62fb07a624e10c593893596cef97959e'
    twilio_number = '+447700104445'
    
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    # Compose the message
    message_body = f"Your OTP for verification is: {otp}"
    
    # Send the SMS
    client.messages.create(from_=twilio_number, body=message_body, to=mobile_number)


def verify_order_otp(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        otp_entered = request.POST.get('otp')
        
        # Retrieve the roadside assistance request object
        roadside_request = get_object_or_404(RoadsideAssistanceRequest, id=request_id)
        
        # Check if the entered OTP matches the OTP stored in the request and it's not null
        if roadside_request.otp == otp_entered and roadside_request.otp is not None:
            # Update the roadside assistance request to mark it as verified
            roadside_request.verified = True
            roadside_request.status = 'Completed'  # Adjust the status as needed
            roadside_request.save()

            # Retrieve the assigned worker and update their status
            if roadside_request.assigned_worker:
                worker = roadside_request.assigned_worker
                worker.is_available = True  # Mark worker as available
                worker.save()
            
            # Redirect to a success page or display a success message
            messages.success(request, 'Roadside assistance request verified successfully.')
            return redirect('worker_breakdown')  # Change 'worker_breakdown' to the name of your worker breakdown URL
        else:
            # Display an error message if the OTP is incorrect or null
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('worker_breakdown')

    # Handle the case if the request method is not POST
    messages.error(request, 'Invalid request method.')
    return redirect('worker_breakdown')