from django.db import models
import datetime
from django.db.models.deletion import CASCADE
from therapist.models import NewDisabledDays, Day
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
        print()
        disabled_days = [day.week_day for day in Day.objects.filter(is_disabled=True)]
        appoint = cls.objects.filter(appointment_date=appointment_date, start_time=start_time,is_approved=True)
        pending_appoint = cls.objects.filter(appointment_date=appointment_date, start_time=start_time, choice='P')
        if not appoint.exists() and not pending_appoint.exists() and not appointment_date.weekday() in disabled_days:
            return True
        else:
            return False
    @classmethod
    def can_disable(cls,week_day):
        appoint = cls.objects.filter(appointment_date__week_day=week_day, is_approved=True)
        print(appoint)
        pending_appoint = AppointmentResponse.objects.filter(appointment_date__week_day=week_day, choice='P')
        appoint_response = AppointmentResponse.objects.filter(appointment_date__week_day=week_day, is_approved=True)
        if not appoint.exists() or not pending_appoint.exists() or not appoint_response.exists():
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
        print()
        disabled_days = [day.week_day for day in Day.objects.filter(is_disabled=True)]
        appoint = cls.objects.filter(appointment_date=appointment_date, start_time=start_time,is_approved=True)
        pending_appoint = cls.objects.filter(appointment_date=appointment_date, start_time=start_time, choice='P')
        if not appoint.exists() and not pending_appoint.exists() and not appointment_date.weekday() in disabled_days:
            return True
        else:
            return False
