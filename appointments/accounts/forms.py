from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from appointments.settings import DATE_INPUT_FORMATS
from datetime import date, datetime, timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import password_validators_help_texts
from django.utils.html import format_html, format_html_join



def calculateAge(birth_date):
    today = date.today()
    age = ((today - birth_date).days)//365
    return age >= 18




class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
    def clean_email(self):
       email = self.cleaned_data['email']
       if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email Already exists"))
       return email



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type':'date', 'placeholder':'Select a date','required': True}),
            'phone_number': forms.DateInput(attrs={'required': True}),
        }

        labels = {
            "date_of_birth": _("date of birth"),
            "phone_number": _("Phone Number")
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth:
            if not calculateAge(date_of_birth):
                raise forms.ValidationError(_('you cannot sign up if you are younger than 18'))
        else:    
            raise forms.ValidationError(_('please fill out this field'))
        return date_of_birth

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if Profile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(_('phone exists'))
        return phone_number


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        print(email)
        if User.objects.filter(email=email).exclude(username=self.instance).exists():
            raise forms.ValidationError(_("Email Already exists"))
        return email

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'date_of_birth']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type':'date', 'placeholder':'Select a date', 'required': True}),
            'phone_number': forms.DateInput(attrs={'required': True}),
        }

        labels = {
            "date_of_birth": _("date of birth"),
            "phone_number": _("Phone Number")
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth:
            if not calculateAge(date_of_birth):
                raise forms.ValidationError(_('you cannot sign up if you are younger than 18'))
        else:
            raise forms.ValidationError(_('please fill out this field'))
        return date_of_birth

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        print(phone_number)
        if Profile.objects.filter(phone_number=phone_number).exclude(user=self.instance.user).exists():
            raise forms.ValidationError(_('phone exists'))
        return phone_number






class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('username'), 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '*********',
        }
))
