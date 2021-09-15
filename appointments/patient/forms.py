from accounts.models import Profile
import datetime
from datetime import datetime
from django import forms
from django.db import models
from .models import Appointment, AppointmentResponse
from datetime import time, date
from django.contrib.auth.models import User
from therapist.models import WorkingTime, Day, Date


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
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date <= date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        elif appointment_date.weekday() in Day.disabled_days() or appointment_date in Date.disabled_dates():
            raise forms.ValidationError('you cannot ask for a meeting for that day')
        return appointment_date