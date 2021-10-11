
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointments.settings')
django.setup()

from django.contrib.sites.models import Site
from therapist.models import WorkingTime, Day
from patient.models import Appointment, AppointmentResponse
from datetime import datetime, time
from patient.models import Appointment, AppointmentResponse
from therapist.models import Day, Comment
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# import pandas as pd
def edit_site():
    site = Site.objects.get_or_create(id=1)
    site.domain = 'appointmentsd.herokuapp.com'
    site.name= 'herokuapp.com'
    site.save()

# edit_site()


def create_day_choice():
    day_li = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    x = [(index, value) for index, value in enumerate(day_li)]
    for item in x:
        Day.objects.get_or_create(week_day=item[0], name=item[1])
# create_day_choice()

def create_working_time():
    WorkingTime.objects.get_or_create(start_time=time(hour=6, minute=30, tzinfo=timezone.utc), end_time=time(hour=16, minute=30, tzinfo=timezone.utc))

# create_working_time()

