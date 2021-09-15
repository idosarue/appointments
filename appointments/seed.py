
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointments.settings')
django.setup()

from django.contrib.sites.models import Site
from therapist.models import WorkingTime, Day
from datetime import datetime, time, timedelta
from patient.models import Appointment, AppointmentResponse
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