from django.db import models
from datetime import date
from django.db.models.deletion import CASCADE
from django.utils.regex_helper import Choice
from therapist.models import Day
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
    is_cancelled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    date_t = models.DateTimeField(null=True)
    week_day = models.ForeignKey('therapist.Day', on_delete=models.CASCADE, null=True)

    @classmethod
    def is_vacant(cls, start_time, appointment_date, end_time):
        appoint = cls.objects.filter(appointment_date=appointment_date, end_time__gte=start_time, start_time__lte=end_time, is_approved=True, is_cancelled=False).exists()
        if not appoint and not appointment_date.weekday() in Day.disabled_days():
            print('true')
            return True
        else:
            print('not')

            return False


    @classmethod
    def can_disable(cls,week_day):
        appoints = [appoint.appointment_date.weekday() for appoint in cls.objects.filter(is_approved=True, is_cancelled=False)]
        if not week_day in appoints:
            return True
        else:
            return False    

    @classmethod
    def valid_appoint(cls, **kwargs):
        appoints = cls.objects.filter(is_cancelled=False, is_approved=True, **kwargs)
        print(kwargs, '44')
        if appoints.exists():
            print('true')
            return True
        else:
            return False

    @classmethod
    def display(cls, **kwargs):
        appoints = cls.objects.filter(is_cancelled=False, is_approved=True, **kwargs)
        return appoints.order_by('start_time')

class AppointmentResponse(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField(null=True)
    appointment_date = models.DateField(auto_now_add=False)
    date_t = models.DateTimeField(null=True)
    original_request = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    choice = models.CharField(choices=CHOICES, null=True, max_length=10) 
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    week_day = models.ForeignKey('therapist.Day', on_delete=models.CASCADE, null=True)
    
    @property
    def is_past_due(self):
        return date.today() < self.appointment_date

    @classmethod
    def is_vacant(cls, start_time, appointment_date, end_time):
        print()
        appoint = cls.objects.filter(appointment_date=appointment_date, end_time__gte=start_time, start_time__lte=end_time, is_approved=True, is_cancelled=False).exists()
        pending_appoint = cls.objects.filter(appointment_date=appointment_date, end_time__gte=start_time, start_time__lte=end_time, choice='P', is_cancelled=False).exists()
        if not appoint and not pending_appoint and not appointment_date.weekday() in Day.disabled_days():
            return True
        else:
            return False

    @classmethod
    def can_disable(cls,week_day):
        appoints = [appoint.appointment_date.weekday() for appoint in cls.objects.filter(is_approved=True, is_cancelled=False)]
        pend_appoints = [appoint.appointment_date.weekday() for appoint in cls.objects.filter(choice='P', is_cancelled=False)]
        print(pend_appoints)
        print(appoints)
        if not week_day in appoints and not week_day in pend_appoints:
            return True
        else:
            return False    

    @classmethod
    def valid_appoint(cls, **kwargs):
        appoints = cls.objects.filter(is_cancelled=False, is_approved=True, **kwargs)
        if appoints.exists():
            return True
        else:
            return False

    @classmethod
    def valid_pending_appoint(cls, **kwargs):
        appoints = cls.objects.filter(is_cancelled=False,choice='P', **kwargs)
        if appoints.exists():
            return True
        else:
            return False
            
    @classmethod
    def display(cls, **kwargs):
        appoints = cls.objects.filter(is_cancelled=False, is_approved=True, **kwargs)
        return appoints.order_by('start_time')
 


    
class ContactUsersMessagesToTherapist(models.Model):
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)