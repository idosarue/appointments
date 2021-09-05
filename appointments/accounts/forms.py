from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from appointments.settings import DATE_INPUT_FORMATS

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class':'datepicker', 'placeholder':'Select a date', 'type':'date'}),
        }
