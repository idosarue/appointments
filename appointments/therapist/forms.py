from django import forms
from django.db import models
from patient.models import *
from patient.forms import appointment_date_validation, HOUR_CHOICES
from django.contrib.auth.models import User
from datetime import date, time
from accounts.models import Profile

def appointment_update_date_validation(appointment_date, start_time, disabled_days, instance):
    print(appointment_date.weekday())
    original_appointment = AppointmentResponse.objects.filter(start_time=start_time, appointment_date=appointment_date, is_approved=True)
    appointment = Appointment.objects.filter(start_time=start_time, appointment_date=appointment_date, is_approved=True)
    pending_original_appointment = AppointmentResponse.objects.filter(start_time=start_time, appointment_date=appointment_date, choice='P')
    if appointment.exists() or original_appointment.exists() or pending_original_appointment.exists():
        if not instance.start_time == start_time or not instance.appointment_date == appointment_date: # if the time for the appointment is the same we can safely change the user
            raise forms.ValidationError('No Available Appointments for date and time specified. please choose another another time or date')
    elif appointment_date.weekday() in disabled_days:
        raise forms.ValidationError('you cannot ask for a meeting on a weekend')
    elif appointment_date <= date.today():
        raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
    return appointment_date

YEAR_CHOICES = [(x+2021,y) for x,y in enumerate(list(range(2021,2051)))]
month_li = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
MONTH_CHOICES = [(x,y) for x,y in enumerate(month_li, 1)]
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
        disabled_days = [4,5]
        date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return date


class EditAppointmentResponseForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.exclude(is_superuser=True))
    class Meta:
        model = AppointmentResponse
        exclude = ['is_approved', 'choice']

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
        new_user = self.cleaned_data['user']
        disabled_days = [4,5]
        date = appointment_update_date_validation(appointment_date, start_time, disabled_days, self.instance)
        return date


    
class EditAppointmentForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Profile.objects.exclude(id=1))
    class Meta:
        model = Appointment
        exclude = ['is_approved', 'choice']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
            'start_time': forms.Select(choices=HOUR_CHOICES),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < time(9,30,00) or start_time > time(16,30,00):
            raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        a = self.instance
        print(a, 'asd')
        return start_time

    def clean_appointment_date(self):
        start_time = self.clean_start_time()
        appointment_date = self.cleaned_data['appointment_date']
        disabled_days = [4,5]
        date = appointment_update_date_validation(appointment_date, start_time, disabled_days, self.instance)
        return date

