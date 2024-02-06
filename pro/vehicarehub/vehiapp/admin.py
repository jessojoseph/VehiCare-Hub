from django.contrib import admin
from .models import CustomUser,Service,UserProfile,Appointment,Slot,Worker,Task,AudioRecording,LeaveRequest,Payment,ServicePrediction, ServiceTimePrediction, Advisor,Category,Policy,PolicyRecord, AccidentClaim


admin.site.register(CustomUser)
admin.site.register(Service)
admin.site.register(UserProfile)
admin.site.register(Appointment)
admin.site.register(Slot)
admin.site.register(Worker)
admin.site.register(LeaveRequest)
admin.site.register(Payment)
admin.site.register(ServicePrediction)
admin.site.register(ServiceTimePrediction)

admin.site.register(Task)
admin.site.register(AudioRecording)


admin.site.register(Advisor)
admin.site.register(Category)
admin.site.register(Policy)
admin.site.register(PolicyRecord)
admin.site.register(AccidentClaim)
