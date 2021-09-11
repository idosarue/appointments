from django import forms
from django.db import models
from django.db.models import fields
from django.forms import widgets
from patient.models import *
from .models import DisabledDays, WorkingTime
from patient.forms import appointment_date_validation
from datetime import date, time
from therapist.models import DisabledDays, WorkingTime

minutes = WorkingTime.objects.first().minutes
start_time = WorkingTime.objects.first().start_time
end_time = WorkingTime.objects.first().end_time

HOUR_CHOICES = [(time(hour=x, minute=minutes), f'{x:02d}:{minutes}') for x in range(start_time, end_time +1)]

day_li = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

DAY_CHOICES = [(x,y) for x,y in enumerate(day_li)]

YEAR_CHOICES = [(x+2021,y) for x,y in enumerate(list(range(2021,2051)))]

month_li = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

MONTH_CHOICES = [(x,y) for x,y in enumerate(month_li, 1)]

days = DisabledDays.objects.last()
disabled_days = [int(x) for x in days.days if x.isnumeric()]


class CalendarForm(forms.Form):
    year = forms.ChoiceField(choices = YEAR_CHOICES)
    month = forms.ChoiceField(choices = MONTH_CHOICES)

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
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date


class EditAppointmentResponseForm(forms.ModelForm):
    class Meta:
        model = AppointmentResponse
        exclude = ['user', 'is_approved', 'choice','original_request']

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
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date

    
class EditAppointmentForm(forms.ModelForm):
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
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date


class TherapistCreateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start_time','user', 'appointment_date']

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
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date


class DisabledDaysForm(forms.ModelForm):
    class Meta:
        model = DisabledDays
        fields = ['days']
        widgets = {
            'days': forms.SelectMultiple(choices=DAY_CHOICES),
        }




class WorkingTimeForm(forms.ModelForm):
    class Meta:
        model = WorkingTime
        fields = '__all__'
    