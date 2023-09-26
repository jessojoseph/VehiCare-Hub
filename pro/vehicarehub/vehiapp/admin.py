from django.contrib import admin
from .models import CustomUser,Service,UserProfile,Appointment,Slot,Worker,Task,AudioRecording,LeaveRequest
from .forms import TaskAssignmentForm  # Import the custom form

admin.site.register(CustomUser)
admin.site.register(Service)
admin.site.register(UserProfile)
admin.site.register(Appointment)
admin.site.register(Slot)
admin.site.register(Worker)
admin.site.register(LeaveRequest)


admin.site.register(Task)
admin.site.register(AudioRecording)