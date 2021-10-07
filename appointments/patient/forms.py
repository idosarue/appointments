from accounts.models import Profile
import datetime
from datetime import datetime
from django import forms
from django.db import models
from .models import Appointment, AppointmentResponse, ContactUsersMessagesToTherapist
from datetime import time, date
from django.contrib.auth.models import User
from therapist.models import WorkingTime, Day, Date
import django_filters
from django.utils.translation import ugettext_lazy as _

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].choices = WorkingTime.create_time_choice()
        
    start_time = forms.ChoiceField()
    class Meta:
        model = Appointment
        fields = ['start_time', 'appointment_date']

 
    
    # def clean_start_time(self):
    #     start = self.cleaned_data['start_time']
    #     start_time = WorkingTime.objects.first().start_time
    #     end_time = WorkingTime.objects.first().end_time
    #     minutes = WorkingTime.objects.first().minutes
    #     choices = [(time(hour=x, minute=minutes, second=00)) for x in range(start_time, end_time +1)]
    #     if datetime.strptime(start, '%H:%M:%S').time() not in choices:
    #         raise forms.ValidationError('Only choose times between 9am and 16:30pm')
    #     return start


    def clean_appointment_date(self):
        data = self.cleaned_data
        appointment_date = data['appointment_date']

        try:
            start_time = data['start_time']
            start = datetime.strptime(start_time, '%H:%M:%S').time()
            end_time = time(hour = start.hour + 1, minute=start.minute)
        except KeyError:
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        if appointment_date <= date.today():
            raise forms.ValidationError('you cannot ask for a meeting for today or a past date')
        elif appointment_date.weekday() in Day.disabled_days():
            raise forms.ValidationError('you cannot ask for a meeting for that day')
        if not Appointment.is_vacant(start_time, appointment_date, end_time) or not AppointmentResponse.is_vacant(start_time, appointment_date, end_time):
            raise forms.ValidationError('no available mettings for that date and time')
        return appointment_date

class UserAppointmentFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['appointment_date'].widget.attrs['id'] = 'filter'
        self.form.fields['appointment_date'].label = _('appointment date')

    appointment_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'type':'date', 'placeholder':'Select a date', 'autocomplete':'off'}))
    class Meta:
        model = Appointment
        fields = ['appointment_date']


class ContactFormEmailPatient(forms.ModelForm):
    class Meta:
        model = ContactUsersMessagesToTherapist
        fields = '__all__'

        widgets = {
            'message' : forms.Textarea()
        }

        labels = {
            'subject' : _('Subject'),
            'message' : _('Message'),
            'email' : _('Email'),
        }