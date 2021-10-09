
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
from django.utils.translation import gettext_lazy as _

# import pandas as pd
def edit_site():
    site = Site.objects.get(id=1)
    site.domain = '127.0.0.1:8000'
    site.name= 'my_site.com'
    site.save()

# edit_site()


def create_day_choice():
    day_li = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    x = [(index, value) for index, value in enumerate(day_li)]
    for item in x:
        Day.objects.create(week_day=item[0], name=item[1])
create_day_choice()

def create_working_time():
    WorkingTime.objects.create(start_time=time(hour=8, minute=30), end_time=time(hour=16, minute=30))

create_working_time()

def create_date_t():
  
    for appoint in Appointment.objects.all():
        appoint.date_t = datetime(
        appoint.appointment_date.year,
        appoint.appointment_date.month,
        appoint.appointment_date.day,
        appoint.start_time.hour,
        appoint.start_time.minute)
        appoint.save()
    for appoint in AppointmentResponse.objects.all():
        appoint.date_t = datetime(
        appoint.appointment_date.year,
        appoint.appointment_date.month,
        appoint.appointment_date.day,
        appoint.start_time.hour,
        appoint.start_time.minute)
        appoint.save()
# create_date_t()
# a_start= '9:30'
# a_end = '10:30'
# b_start = '10:30'
'930'
'1045'
'12'
# def new_is_vacant(cls, start_time, appointment_date, end_time):
#     print()
#     appoint = cls.valid_appoint(appointment_date=appointment_date, end_time__lte=start_time)
#     # pending_appoint = AppointmentResponse.valid_pending_appoint(appointment_date=appointment_date, start_time=start_time)
#     if not appoint and not appointment_date.weekday() in Day.disabled_days():
#         return True
#     else:
#         return False'
'930'
'1045'
'12'
# events = Appointment.display(appointment_date__year=self.year, appointment_date__month=self.month)
# events2 = AppointmentResponse.display(appointment_date__year=self.year, appointment_date__month=self.month)
# comments = Comment.objects.filter(date__year=self.year, date__month=self.month, is_deleted=False)



