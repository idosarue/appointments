from django.db import models

# Create your models here.
class DisabledDays(models.Model):
    days = models.CharField(null=True, max_length=200)
    is_disabled = models.BooleanField(default=False)
