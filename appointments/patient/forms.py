from django import forms
from django.db import models
from .models import Appointment
from datetime import time

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['user', 'is_approved']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'class':'datepicker', 'placeholder':'Select a date', 'type':'date'}),
            'start_time': forms.DateInput(attrs={'class':'timepicker', 'type':'time'}),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < time(9,00,00) or start_time > time(16,30,00):
            raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start_time