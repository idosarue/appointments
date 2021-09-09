import datetime
from django import forms
from django.db import models
from .models import Appointment, AppointmentResponse
from datetime import time

HOUR_CHOICES = [(time(hour=x, minute=30), f'{x:02d}:30') for x in range(9, 17)]

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
        original_appointment = AppointmentResponse.objects.filter(start_time=start_time, appointment_date=appointment_date, is_approved=True).exists()
        appointment = Appointment.objects.filter(start_time=start_time, appointment_date=appointment_date, is_approved=True).exists()
        if appointment or original_appointment:
            raise forms.ValidationError('No Available Appointments for date and time specified. please choose another another time or date')
        elif appointment_date <= datetime.date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        return appointment_date

class AppointmentResponseForm(forms.ModelForm):
    class Meta:
        model = AppointmentResponse
        fields = ['start_time', 'appointment_date']

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
        appointment_date = self.cleaned_data['appointment_date']
        start_time = self.clean_start_time()
        original_appointment = AppointmentResponse.objects.filter(start_time=start_time, appointment_date=appointment_date, is_approved=True).exists()
        appointment = Appointment.objects.filter(start_time=start_time, appointment_date=appointment_date, is_approved=True).exists()
        if appointment or original_appointment:
            raise forms.ValidationError('No Available Appointments for date and time specified. please choose another another time or date')
        if appointment_date <= datetime.date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        return appointment_date

