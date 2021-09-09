from django.http.response import HttpResponse
from patient.models import Appointment, AppointmentResponse
from accounts.models import Profile
from django.db import models
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from .forms import AppointmentForm, AppointmentResponseForm
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from send_emails import message_to_therapist, message_to_user

# Create your views here.
def home(request):
    return render(request, 'patient/home.html')

class CreateAppointmentView(LoginRequiredMixin, CreateView):
    form_class = AppointmentForm
    template_name = 'patient/query_appointment.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        appoint = form.save(commit=False)
        appoint.user = self.request.user.profile
        appoint.save()
        message_to_user(self.request.user, form.cleaned_data['start_time'], form.cleaned_data['appointment_date'])
        message_to_therapist(self.request.user, form.cleaned_data['start_time'], form.cleaned_data['appointment_date'], 'testdjangosaru@gmail.com')
        return super().form_valid(form)

class FutureAppointmentsListView(ListView):
    model = Appointment
    template_name = 'patient/future_appointments_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(is_approved=True, user=self.request.user.profile, appointment_date__gte = datetime.today())
        context['appointments_response'] = AppointmentResponse.objects.filter(is_approved=True, user=self.request.user.profile, appointment_date__gte = datetime.today())
        return context

class PastAppointmentsListView(ListView):
    model = Appointment
    template_name = 'patient/past_appointments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(is_approved=True, user=self.request.user.profile, appointment_date__lt = datetime.today())
        context['appointments_response'] = AppointmentResponse.objects.filter(is_approved=True, user=self.request.user.profile, appointment_date__lt = datetime.today())
        return context


