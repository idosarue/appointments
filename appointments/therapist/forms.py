from django import forms
from django.db import models
from django.db.models import fields
from django.forms import widgets
from patient.models import *
from patient.forms import appointment_date_validation
from datetime import date, time, datetime
from .models import NewDisabledDays, WorkingTime, Day
from django.forms.widgets import NumberInput


day_li = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

DAY_CHOICES = [(x,y) for x,y in enumerate(day_li)]

YEAR_CHOICES = [(x+2021,y) for x,y in enumerate(list(range(2021,2051)))]

month_li = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

MONTH_CHOICES = [(x,y) for x,y in enumerate(month_li, 1)]

# days = NewDisabledDays.objects.last()
# disabled_days = [int(x) for x in days.days if x.isnumeric()]


class CalendarForm(forms.Form):
    year = forms.ChoiceField(choices = YEAR_CHOICES)
    month = forms.ChoiceField(choices = MONTH_CHOICES)

class AppointmentResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        self.fields['start_time'].choices = [(time(hour=x, minute=00), f'{x:02d}:00') for x in range(start_time, end_time +1)]
    start_time = forms.ChoiceField()
    class Meta:
        model = AppointmentResponse
        fields = ['start_time', 'appointment_date']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
        }
        

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time'].value
        print(type(start_time))
        for item in start_time:           
            if time(item[0]) < time(9,30,00) or time(item[0]) > time(16,30,00):
                raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start_time


    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        start_time = self.clean_start_time()
        # date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return appointment_date


class EditAppointmentResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        self.fields['start_time'].choices = [(time(hour=x, minute=00), f'{x:02d}:00') for x in range(start_time, end_time +1)]
    start_time = forms.ChoiceField()
    class Meta:
        model = AppointmentResponse
        exclude = ['user', 'is_approved', 'choice','original_request']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
            # 'start_time': forms.Select(choices=HOUR_CHOICES),
        }
    def clean_start_time(self):
        start_time = self.cleaned_data['start_time'].value
        for item in start_time:           
            if time(item[0].hour, item[0].minute, item[0].second) < time(9,30,00) or time(item[0].hour, item[0].minute, item[0].second) > time(16,30,00):
                raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start_time


    def clean_appointment_date(self):
        start_time = self.clean_start_time()
        appointment_date = self.cleaned_data['appointment_date']
        # date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return start_time

    
class EditAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        self.fields['start_time'].choices = [(time(hour=x, minute=00), f'{x:02d}:00') for x in range(start_time, end_time +1)]
    start_time = forms.ChoiceField()
    class Meta:
        model = Appointment
        exclude = ['user', 'is_approved', 'choice']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        for item in start_time:           
            if time(item[0].hour, item[0].minute, item[0].second) < time(9,30,00) or time(item[0].hour, item[0].minute, item[0].second) > time(16,30,00):
                raise forms.ValidationError('Only choose times between 9am and 16:30pm')
        return start_time


    def clean_appointment_date(self):
        start_time = self.clean_start_time()
        appointment_date = self.cleaned_data['appointment_date']
        # date = appointment_date_validation(appointment_date, start_time, disabled_days)
        return start_time


class TherapistCreateAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        self.fields['start_time'].choices = [(time(hour=x, minute=00), f'{x:02d}:00') for x in range(start_time, end_time +1)]
    start_time = forms.ChoiceField()
    class Meta:
        model = Appointment
        fields = ['start_time','user', 'appointment_date']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
        }


    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date <= date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        return appointment_date


class DisabledDaysForm(forms.ModelForm):
    # day = forms.ModelMultipleChoiceField(queryset=Day.objects.all())
    class Meta:
        model = NewDisabledDays
        fields = ['day']


class WorkingTimeForm(forms.ModelForm):

    class Meta:
        model = WorkingTime
        fields = '__all__'
    
        help_texts = {
            'start_time': ('set hour from 1 to 24'),
            'end_time': ('set hour from 1 to 24'),
        }
    def clean(self):
        data = self.cleaned_data
        start_time = data['start_time']
        end_time = data['end_time']
        if end_time <= 0:
            raise forms.ValidationError('you cannot set your end time to 0 or less')
        elif start_time <= 0:
            raise forms.ValidationError('you cannot set your start time to 0 or less')
        elif start_time > 24:
            raise forms.ValidationError('hour doesn\'t exist')
        elif end_time <= start_time:
            raise forms.ValidationError('end time must be bigger than your start time')
        elif start_time >= end_time:
            raise forms.ValidationError('start time must be bigger than your end time')
        elif end_time > 24:
            raise forms.ValidationError('hour doesn\'t exist')
        return data