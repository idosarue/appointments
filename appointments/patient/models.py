from django.db import models

# Create your models here.
class Appointment(models.Model):
    start_time = models.TimeField()
    appointment_date = models.DateField()
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, null=True)

