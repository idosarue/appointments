
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointments.settings')
django.setup()

from django.contrib.sites.models import Site
from therapist.models import WorkingTime, Day
from datetime import date, datetime, time, timedelta
from patient.models import Appointment, AppointmentResponse
from functools import reduce

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
# create_day_choice()

def create_working_time():
    WorkingTime.objects.create()

# create_working_time()

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
print(datetime.today().date())
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

def create_time_choice():
    c = 0
    break_time = 15
    new_li = []
    li = []
    start_time = WorkingTime.objects.first().start_time
    end_time = WorkingTime.objects.first().end_time
    minutes = 30
    for x in range(start_time , end_time +1):
        y = datetime.combine(date.today(),time(hour=x, minute=minutes))+timedelta(minutes=c)
        if y.time().hour >= end_time +1:
            if li[-1].minute > minutes:
                x = li.pop()
                y = time(hour=end_time, minute=li[-1].minute)
                li.insert(len(li),y)
            return li
        li.append(y.time())
        c+=break_time
print(create_time_choice())
# # print(timedelta)
# '7:33'
# '8:48'
# '9:03'
# x = datetime.combine(date.today(),time(hour=8,minute=15))+ timedelta(minutes=15)
# print(x.time())
# start_time = WorkingTime.objects.first().start_time
# end_time = WorkingTime.objects.first().end_time
# minutes = 15
# x = [datetime.combine(date.today(),time(hour=x, minute=minutes)) for x in range(start_time, end_time +1)]
# for i in x:
#     i += timedelta(minutes=15)
#     print(i)
