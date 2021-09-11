import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointments.settings')
django.setup()

from django.contrib.sites.models import Site
from therapist.models import DisabledDays, WorkingTime

def edit_site():
    site = Site.objects.get(id=1)
    site.domain = '127.0.0.1:8000'
    site.name= 'my_site.com'
    site.save()

# edit_site()

# def create_day_choice():
#     day_num_li = list(range(7))
#     days = DisabledDays.objects.create(days=day_num_li)
#     return days
# create_day_choice()

def create_working_time():
    WorkingTime.objects.create()

# create_working_time()