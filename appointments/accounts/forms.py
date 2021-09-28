from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from appointments.settings import DATE_INPUT_FORMATS
from datetime import date

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
            raise forms.ValidationError("Email exists")
       return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type':'date', 'placeholder':'Select a date'}),
        }
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if not calculateAge(date_of_birth):
            raise forms.ValidationError('you cannot sign up if you are younger than 18')
        return date_of_birth

        
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if Profile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('phone exists')
        return phone_number


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        print(email)
        if User.objects.filter(email=email).exclude(username=self.instance).exists():
            raise forms.ValidationError("Email Already exists")
        return email

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'date_of_birth']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type':'date', 'placeholder':'Select a date'}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if not calculateAge(date_of_birth):
            raise forms.ValidationError('you cannot sign up if you are younger than 18')
        return date_of_birth

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        print(phone_number)
        if Profile.objects.filter(phone_number=phone_number).exclude(user=self.instance.user).exists():
            raise forms.ValidationError('phone exists')
        return phone_number



    
