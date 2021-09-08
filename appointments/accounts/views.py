from .models import Profile
from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import ProfileForm, SignupForm, ValidationForm, EditUserForm, EditProfileForm
from django.views.generic import CreateView, DetailView, FormView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import login, authenticate
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        profile_form = ProfileForm(self.request.POST)
        if profile_form.is_valid():
            form.save()
            user = authenticate(self.request, username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email=form.cleaned_data['email'], password=form.cleaned_data['password1'] )   
            if user:
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                login(self.request, user)
            else:
                messages.error(self.request, 'Something went wrong')
        else:
            return self.form_invalid(form)

        return redirect('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileForm()
        return context

class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

class MyLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            if user.is_superuser:
                return redirect('home')
            else:
                return redirect('profile')
        return super().form_valid(form)

class ValidationView(FormView):
    form_class = ValidationForm
    template_name = 'accounts/verification.html'


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
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Your password was changed successfully')
        return super().form_valid(form)