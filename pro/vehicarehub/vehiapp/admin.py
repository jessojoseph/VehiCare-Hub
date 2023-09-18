from django.contrib import admin
from .models import CustomUser,Service,UserProfile,Appointment,Slot,Worker

admin.site.register(CustomUser)
admin.site.register(Service)
admin.site.register(UserProfile)
admin.site.register(Appointment)
admin.site.register(Slot)
admin.site.register(Worker)