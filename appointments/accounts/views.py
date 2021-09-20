from .models import Profile
from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import ProfileForm, SignupForm, EditUserForm, EditProfileForm
from django.views.generic import CreateView, DetailView, FormView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
# Create your views here.
class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save()
        profile_form = ProfileForm(self.request.POST, instance=user.profile)
        if profile_form.is_valid():
            user = authenticate(self.request, username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email=form.cleaned_data['email'], password=form.cleaned_data['password1'] )   
            if user:
                login(self.request, user)
            else:
                messages.error(self.request, 'Something went wrong')
        else:
            user.delete()
            return self.form_invalid(form)

        return redirect('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileForm(self.request.POST or None)
        return context

class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile



class MyLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self) :
        if self.request.user.is_superuser:
            return reverse_lazy('calendar') 
        else:
            return super().get_success_url()

class ValidationView(FormView):
    pass


class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = EditUserForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = EditUserForm(instance=self.request.user)
        context['profile_form'] = EditProfileForm(instance=self.request.user.profile)
        return context
            
    def form_valid(self, form):
        user_form = EditUserForm(self.request.POST, instance=self.request.user)
        profile_form = EditProfileForm(self.request.POST, instance=self.request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return super().form_valid(form)

class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your password was changed successfully')
        return super().form_valid(form)
    