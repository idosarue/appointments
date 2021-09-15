from django.http.response import HttpResponse
from patient.models import Appointment, AppointmentResponse
from accounts.models import Profile
from django.db import models
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from .forms import AppointmentForm
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from send_emails import (send_message_to_therapist, 
send_message_to_user, 
send_message_to_therapist_after_update)

# Create your views here.
def home(request):
    return render(request, 'patient/home.html')

class CreateAppointmentView(LoginRequiredMixin, CreateView):
    form_class = AppointmentForm
    template_name = 'patient/query_appointment.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        if not Appointment.is_vacant(start_time=form.cleaned_data['start_time'], appointment_date=form.cleaned_data['appointment_date']):
            messages.error(self.request, 'no available meetings for that date or time, please choose another date or time')
            return super().form_invalid(form)
        appoint = form.save(commit=False)
        appoint.user = self.request.user.profile
        x = datetime(
            appoint.appointment_date.year,
            appoint.appointment_date.month,
            appoint.appointment_date.day,
            appoint.start_time.hour,
            appoint.start_time.minute,
            )
        appoint.date_t = x
        appoint.save()
        send_message_to_user(self.request.user, form.cleaned_data['start_time'], form.cleaned_data['appointment_date'])
        send_message_to_therapist(self.request.user, form.cleaned_data['start_time'], form.cleaned_data['appointment_date'])
        return super().form_valid(form)

class CreateAppointmentViewAfterUpdate(LoginRequiredMixin, CreateView):
    form_class = AppointmentForm
    template_name = 'patient/query_appointment.html'
    success_url = reverse_lazy('profile')
        
    def get_appointment(self):
        appoint_id = self.kwargs['pk']
        return get_object_or_404(AppointmentResponse, id=appoint_id)

    def form_valid(self, form):
        appoint = form.save(commit=False)
        appoint.user = self.request.user.profile
        original_appointment = self.get_appointment() 
        original_appointment.choice = 'R'
        original_appointment.save()
        appoint.save()
        send_message_to_therapist_after_update(original_appointment, self.request.user, appoint)
        send_message_to_user(self.request.user, form.cleaned_data['start_time'], form.cleaned_data['appointment_date'])
        return super().form_valid(form)


class FutureAppointmentsListView(ListView):
    model = Appointment
    template_name = 'patient/future_appointments_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = datetime(2021,11,11, 11,11,11)
        print(a)
        appoint = Appointment.display(user=self.request.user.profile, date_t__gt = datetime.today())
        appoint_response = AppointmentResponse.display(user=self.request.user.profile, date_t__gt = datetime.today())
        if appoint:
            context['appointments'] = appoint
        if appoint_response:
            context['appointments_response'] = appoint_response
        return context

class PastAppointmentsListView(ListView):
    model = Appointment
    template_name = 'patient/past_appointments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appoint = Appointment.display(user=self.request.user.profile, date_t__lt=datetime.today())
        appoint_response = AppointmentResponse.display(user=self.request.user.profile, date_t__lt=datetime.today())
        context['appointments'] = appoint
        context['appointments_response'] = appoint_response
        return context


