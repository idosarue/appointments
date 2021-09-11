from accounts.models import Profile
import datetime
from django import forms
from django.db import models
from .models import Appointment, AppointmentResponse
from datetime import time, date
from django.contrib.auth.models import User
from therapist.models import DisabledDays, WorkingTime

minutes = WorkingTime.objects.first().minutes
start_time = WorkingTime.objects.first().start_time
end_time = WorkingTime.objects.first().end_time

HOUR_CHOICES = [(time(hour=x, minute=minutes), f'{x:02d}:{minutes}') for x in range(start_time, end_time + 1)]

def appointment_date_validation(appointment_date, start_time, disabled_days):
    print(appointment_date.weekday())
    original_appointment = AppointmentResponse.objects.filter(start_time=start_time, appointment_date=appointment_date, is_approved=True).exists()
    appointment = Appointment.objects.filter(start_time=start_time, appointment_date=appointment_date, is_approved=True).exists()
    pending_original_appointment = AppointmentResponse.objects.filter(start_time=start_time, appointment_date=appointment_date, choice='P').exists()
    if appointment or original_appointment or pending_original_appointment:
        raise forms.ValidationError('No Available Appointments for date and time specified. please choose another another time or date')
    elif appointment_date.weekday() in disabled_days:
        raise forms.ValidationError('you cannot ask for a meeting on that day')
    elif appointment_date <= date.today():
        raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
    return appointment_date

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['user', 'is_approved', 'choice']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
            'start_time': forms.Select(choices=HOUR_CHOICES),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < time(9,30,00) or start_time > time(16,30,00):
            raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start_time

    def clean_appointment_date(self):
        start_time = self.clean_start_time()
        appointment_date = self.cleaned_data['appointment_date']
        days = DisabledDays.objects.first()
        disabled_days = [int(x) for x in days.days if x.isnumeric()]
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date


