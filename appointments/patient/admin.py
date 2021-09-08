from django.contrib import admin
from .models import Appointment, AppointmentResponse

# Register your models here.
admin.site.register(Appointment)
admin.site.register(AppointmentResponse)