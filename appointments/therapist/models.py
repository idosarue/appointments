# from patient.models import Appointment, AppointmentResponse
from django.db import models

# Create your models here.

class Day(models.Model):
    name = models.CharField(max_length=200)
    week_day = models.IntegerField(default=0) 
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class NewDisabledDays(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)

    def __str__(self):
        return self.day.name

class WorkingTime(models.Model):
    start_time = models.IntegerField(default=9)
    end_time = models.IntegerField(default=16)

        
