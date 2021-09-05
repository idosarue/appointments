from .models import Profile
from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import ProfileForm, SignupForm
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        form.save()
        user = authenticate(self.request, username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email=form.cleaned_data['email'], password=form.cleaned_data['password1'] )   
        if user:
            profile_form = ProfileForm(self.request.POST)
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                login(self.request, user)
            else:
                print('not')
                messages.error(self.request, 'Something went wrong')
        else:
            messages.error(self.request, 'Something went wrong')
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
