from accounts.models import Profile
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.utils.regex_helper import Choice
from patient.models import *
from datetime import date, time, datetime
from .models import Date, WorkingTime, Day
from django.forms.widgets import NumberInput
import django_filters
from django.core.paginator import Paginator

class CalendarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].choices = [(x+2021,y) for x,y in enumerate(list(range(2021,2051)))]
        month_li = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.fields['month'].choices = [(x,y) for x,y in enumerate(month_li, 1)]
    year = forms.ChoiceField()
    month = forms.ChoiceField()

class AppointmentResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        minutes = WorkingTime.objects.first().minutes
        if minutes == 0:
            display_minutes = '00'
        else:
            display_minutes = minutes
        self.fields['start_time'].choices = [(time(hour=x, minute=minutes), f'{x:02d}:{display_minutes}') for x in range(start_time, end_time +1)]
    start_time = forms.ChoiceField()
    start_time = forms.ChoiceField()
    class Meta:
        model = AppointmentResponse
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
            raise forms.ValidationError('Only choose times from choices')
        return start


    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date <= date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        elif appointment_date.weekday() in Day.disabled_days():
            raise forms.ValidationError('you cannot ask for a meeting for that day')
        return appointment_date
    


class EditAppointmentResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        minutes = WorkingTime.objects.first().minutes
        if minutes == 0:
            display_minutes = '00'
        else:
            display_minutes = minutes
        self.fields['start_time'].choices = [(time(hour=x, minute=minutes), f'{x:02d}:{display_minutes}') for x in range(start_time, end_time +1)]
    start_time = forms.ChoiceField()
    class Meta:
        model = AppointmentResponse
        fields = ['start_time', 'appointment_date']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
        }

    def clean_start_time(self):
        start = self.cleaned_data['start_time']
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        choices = [(time(hour=x, minute=00, second=00)) for x in range(start_time, end_time +1)]
        if datetime.strptime(start, '%H:%M:%S').time() not in choices:
            raise forms.ValidationError('Only choose times from choices')
        return start


    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date <= date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        elif appointment_date.weekday() in Day.disabled_days():
            raise forms.ValidationError('you cannot ask for a meeting for that day')
        return appointment_date
    
class EditAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        minutes = WorkingTime.objects.first().minutes
        if minutes == 0:
            display_minutes = '00'
        else:
            display_minutes = minutes
        self.fields['start_time'].choices = [(time(hour=x, minute=minutes), f'{x:02d}:{display_minutes}') for x in range(start_time, end_time +1)]
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
        choices = [(time(hour=x, minute=00, second=00)) for x in range(start_time, end_time +1)]
        if datetime.strptime(start, '%H:%M:%S').time() not in choices:
            raise forms.ValidationError('Only choose times from choices')
        return start


    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date <= date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        elif appointment_date.weekday() in Day.disabled_days():
            raise forms.ValidationError('you cannot ask for a meeting for that day')
        return appointment_date


class TherapistCreateAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        minutes = WorkingTime.objects.first().minutes
        if minutes == 0:
            display_minutes = '00'
        else:
            display_minutes = minutes
        self.fields['start_time'].choices = [(time(hour=x, minute=minutes), f'{x:02d}:{display_minutes}') for x in range(start_time, end_time +1)]
    start_time = forms.ChoiceField()
    class Meta:
        model = Appointment
        fields = ['user', 'start_time', 'appointment_date']

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
            raise forms.ValidationError('Only choose times from choices')
        return start


    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date <= date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        elif appointment_date.weekday() in Day.disabled_days():
            raise forms.ValidationError('you cannot ask for a meeting for that day')
        return appointment_date

class DateInput(forms.DateInput):
    input_type = 'date'
    
class DisabledDatesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for x in self.fields['date'].widget.attrs:
            print(self.fields['date'])
    class Meta:
        model = Date
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'id':'datepicker','placeholder':'Select a date', 'autocomplete':'off',  'onclick':'someFunc()'}),
        }

    def clean_date(self):
        # appoint = 
        d = self.cleaned_data['date']
        if d <= date.today():
            raise forms.ValidationError('day has passed')
        elif d in Date.disabled_dates():
            raise forms.ValidationError('date already disabled')
        elif Appointment.valid_appoint(appointment_date=d) or AppointmentResponse.valid_appoint(appointment_date=d) or AppointmentResponse.valid_pending_appoint(appointment_date=d):
            raise forms.ValidationError('you have appointments for that day')
        return d

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
        minutes = data['minutes']
        print(start_time)
        print(end_time)
        try:
            starting_time = time(hour=start_time, minute=minutes)
            ending_time = time(hour=end_time, minute=minutes)
            print(ending_time)
            apoointment__start_times = Appointment.valid_appoint(start_time__lt=starting_time)
            apoointment_response__start_times = AppointmentResponse.valid_appoint(start_time__lt=starting_time) 
            pending_apoointment__start_times = AppointmentResponse.valid_pending_appoint(start_time__lt=starting_time)
            less_apoointment__end_times = Appointment.valid_appoint(start_time__gt=ending_time)
            less_pending_apoointment__end_times = AppointmentResponse.valid_pending_appoint(start_time__gt=ending_time)
            less_appoointment_response__end_times = AppointmentResponse.valid_appoint(start_time__gt=ending_time)
        except ValueError:
            if start_time >= end_time:
                raise forms.ValidationError('start time must be bigger than your end time')
            elif end_time > 24:
                raise forms.ValidationError('hour doesn\'t exist')
            elif end_time <= 0:
                raise forms.ValidationError('you cannot set your end time to 0 or less')
            elif start_time <= 0:
                raise forms.ValidationError('you cannot set your start time to 0 or less')
            elif start_time > 24:
                raise forms.ValidationError('hour doesn\'t exist')
            elif minutes > 59:
                raise forms.ValidationError('minute doesn\'t exist')
            else:
                raise forms.ValidationError('something terrible happend')

        if apoointment__start_times or apoointment_response__start_times:
            raise forms.ValidationError(f'you have appoitments set before {starting_time}')
        elif less_apoointment__end_times or less_appoointment_response__end_times :
            raise forms.ValidationError(f'you have appoitments set after {ending_time}')
        elif less_pending_apoointment__end_times or pending_apoointment__start_times:
            raise forms.ValidationError('you have appoitments pending for later time')
        elif end_time <= start_time:
            raise forms.ValidationError('end time must be bigger than your start time')

            
        return data

class AppointmentFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['user'].queryset = Profile.objects.exclude(user__is_superuser=True)
    appointment_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date', 'autocomplete':'off'}))
    class Meta:
        model = Appointment
        fields = ['user', 'appointment_date']
        
    # @property
    # def qs(self):
    #     parent = super().qs
    #     x = Appointment.display()
    #     return parent.filter(appointment_date=date.today(), is_cancelled=False, is_)
    
class PendingAppointmentFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['user'].queryset = Profile.objects.exclude(user__is_superuser=True)
    appointment_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date', 'autocomplete':'off'}))
    class Meta:
        model = AppointmentResponse
        fields = ['user', 'appointment_date']


# class AppointmentResponseFilter(django_filters.FilterSet):
#     class Meta:
#         model = AppointmentResponse
#         fields = ['user', 'appointment_date']
#         widgets = {
#             'date': forms.DateInput(attrs={'id':'datepicker', 'placeholder':'Select a date'}),
#         }