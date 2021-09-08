from django.db import models
from datetime import datetime
# Create your models here.
CHOICES = [
    ('A', 'ACCEPT'),
    ('P','PENDING'),
]
class Appointment(models.Model):
    start_time = models.TimeField()
    appointment_date = models.DateField(auto_now_add=False)
    choice = models.CharField(choices=CHOICES, null=True, max_length=10) 
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class AppointmentResponse(models.Model):
    start_time = models.TimeField()
    appointment_date = models.DateField(auto_now_add=False)
    original_request = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False)

    def approve_meeting(self):
        pass

