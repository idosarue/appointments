from django.db import models
import datetime
from django.db.models.deletion import CASCADE
from therapist.models import NewDisabledDays
# Create your models here.
CHOICES = [
    ('A', 'ACCEPT'),
    ('P','PENDING'),
    ('R','REJECTED'),
]
class Appointment(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField(null=True)
    appointment_date = models.DateField(auto_now_add=False)
    choice = models.CharField(choices=CHOICES, null=True, max_length=10) 
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def is_vacant(cls, start_time, appointment_date):
        print(appointment_date.weekday())
        appoint = cls.objects.filter(appointment_date=appointment_date, start_time=start_time,is_approved=True)
        pending_appoint = cls.objects.filter(appointment_date=appointment_date, start_time=start_time, choice='P')
        if not appoint.exists() and not pending_appoint.exists():
            return True
        else:
            return False

class AppointmentResponse(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField(null=True)
    appointment_date = models.DateField(auto_now_add=False)
    original_request = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    choice = models.CharField(choices=CHOICES, null=True, max_length=10) 
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False)



    @classmethod
    def is_vacant(cls, start_time, appointment_date):
        appoint = cls.objects.filter(appointment_date=appointment_date, start_time=start_time,is_approved=True)
        pending_appoint = cls.objects.filter(appointment_date=appointment_date, start_time=start_time, choice='P')
        if not appoint.exists() and not pending_appoint.exists():
            return True
        else:
            return False