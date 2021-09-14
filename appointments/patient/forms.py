from accounts.models import Profile
import datetime
from datetime import datetime
from django import forms
from django.db import models
from .models import Appointment, AppointmentResponse
from datetime import time, date
from django.contrib.auth.models import User
from therapist.models import WorkingTime
from therapist.models import Day

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        minutes = WorkingTime.objects.first().minutes
      
        self.fields['start_time'].choices = [(time(hour=x, minute=minutes), f'{x:02d}:00') for x in range(start_time, end_time +1)]
    start_time = forms.ChoiceField()
    class Meta:
        model = Appointment
        fields = ['start_time', 'appointment_date']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
        }
    
    def clean_start_time(self):
        start = self.cleaned_data['start_time']
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        minutes = WorkingTime.objects.first().minutes
        choices = [(time(hour=x, minute=minutes, second=00)) for x in range(start_time, end_time +1)]
        if datetime.strptime(start, '%H:%M:%S').time() not in choices:
            raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start


    def clean_appointment_date(self):
        disabled_days = [day.week_day for day in Day.objects.filter(is_disabled=True)]
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date <= date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        elif appointment_date.weekday() in disabled_days:
            raise forms.ValidationError('you cannot ask for a meeting for that day')
        return appointment_date