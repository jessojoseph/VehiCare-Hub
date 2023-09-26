from .forms import AppointmentForm
from .forms import ServiceForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .models import Service, UserProfile,Worker,Slot,CustomUser,Appointment
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

from datetime import datetime, timedelta

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Check if there are already 7 appointments for the selected service_date
                service_date = form.cleaned_data['service_date']
                existing_appointments_count = Appointment.objects.filter(
                    service_date=service_date
                ).count()

                if existing_appointments_count >= 7:
                    return render(request, 'book_appointment.html', {'form': form, 'error_message': 'No more slots available for this date.'})

                appointment = form.save(commit=False)
                appointment.user_name = request.user
                appointment.save()

                return redirect('confirmation')
    else:
        form = AppointmentForm()

    # Generate 7 equal time slots starting from 9:00 AM
    base_time = datetime.strptime('09:00', '%H:%M')
    time_slots = [(base_time + timedelta(hours=i)).strftime('%H:%M') for i in range(7)]

    # Get service types from the Service model
    service_types = Service.objects.all()

    return render(request, 'book_appointment.html', {'form': form, 'time_slots': time_slots, 'service_types': service_types})


@login_required
def viewappointment(request):
    if request.user.is_staff:
        # Admin user can view all appointments
        appointments = Appointment.objects.all()
    else:
        # Regular user can only view their own appointments
        appointments = Appointment.objects.filter(user_name=request.user)
    
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
            return redirect('addworker')  # Replace 'adminindex' with your desired URL

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

# def update_work_status(request, task_id):
#     task = get_object_or_404(Task, id=task_id)

#     if request.method == 'POST':
#         # Check if an audio file was uploaded
#         if 'audio_file' in request.FILES:
#             audio_file = request.FILES['audio_file']

#             # Create a recognizer instance
#             recognizer = sr.Recognizer()

#             # Process the audio file
#             with sr.AudioFile(audio_file) as source:
#                 audio = recognizer.record(source)  # Record the audio from the file
#                 try:
#                     # Use Google Web Speech API to recognize the audio
#                     text = recognizer.recognize_google(audio)
#                     # Now 'text' contains the recognized text from the audio
#                 except sr.UnknownValueError:
#                     text = "Speech Recognition could not understand the audio"
#                 except sr.RequestError as e:
#                     text = f"Could not request results from Google Web Speech API; {e}"

#                 # Save the transcription in your task model
#                 task.audio_transcription = text

#         # Update the other task fields with the new values
#         new_status = request.POST.get('new_status').lower()
#         work_done = request.POST.get('work_done')
#         materials_used = request.POST.get('materials_used')
#         additional_notes = request.POST.get('additional_notes')

#         task.status = new_status
#         task.work_done = work_done
#         task.materials_used = materials_used
#         task.additional_notes = additional_notes

#         # Save the task object to update the database
#         task.save()

#         # Redirect to the worker dashboard or any other appropriate page
#         return redirect('workerdashboard')

#     context = {'task': task}
#     return render(request, 'worker/update_work_status.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Worker, Appointment

def update_work_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        work_done = request.POST.get('work_done')
        materials_used = request.POST.get('materials_used')
        additional_notes = request.POST.get('additional_notes')
        audio_data = request.FILES.get('audio_data')

        task.status = new_status
        task.work_done = work_done
        task.materials_used = materials_used
        task.additional_notes = additional_notes

        # Check if audio_data is provided and save it to the database
        if audio_data:
            task.audio_file.save(audio_data.name, audio_data)

        task.save()

        # Check if the task is marked as completed
        if new_status == 'completed':
            # Get the worker associated with the task
            worker = task.worker

            # Mark the worker as available for other jobs
            worker.is_available = True
            worker.save()

        return redirect('workerdashboard')

    return render(request, 'worker/update_work_status.html', {'task': task})


from .models import Task, CustomUser, Appointment

@login_required
def view_updates(request):
    user = request.user  # Get the currently logged-in user
    
    # Check if the user is an admin (you can modify this condition based on your admin role criteria)
    is_admin = user.is_superuser

    appointments = None
    selected_appointment = None

    if is_admin:
        # Fetch all appointments for the admin
        appointments = Appointment.objects.all()

        # Check if a specific appointment is selected from the form
        if request.method == 'POST':
            appointment_id = request.POST.get('appointment')
            if appointment_id:
                selected_appointment = Appointment.objects.get(id=appointment_id)
    else:
        # For regular users, restrict them to only view their own updates
        appointments = Appointment.objects.filter(user_name=user)
        selected_appointment = appointments.first()  # Display the first appointment by default

    tasks = Task.objects.filter(appointment=selected_appointment)

    context = {'appointments': appointments, 'tasks': tasks, 'selected_appointment': selected_appointment, 'is_admin': is_admin}
    return render(request, 'view_updates.html', context)
