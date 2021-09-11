from django.db import models

# Create your models here.
class DisabledDays(models.Model):
    days = models.CharField(null=True, max_length=200)
    is_disabled = models.BooleanField(default=False)

class WorkingTime(models.Model):
    start_time = models.IntegerField(default=9)
    minutes = models.IntegerField(default=30)
    end_time = models.IntegerField(default=16)