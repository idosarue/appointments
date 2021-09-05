from django.db import models
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from patient.models import Appointment
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage
from patient.forms import AppointmentForm, AppointmentResponseForm

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class AppointmentListView(SuperUserRequiredMixin, ListView):
    model = Appointment
    template_name = 'therapist/apt_requests.html'
    context_object_name = 'appointments'
    ordering = 'timestamp'


def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, id=pk)
    therapist_email = 'testdjangosar@gmail.com'
    if status == 'accept':
        appointment.choice = 'A'
        appointment.is_approved = True
        appointment.save()
        email_message_user = f'''
        Hello {appointment.user}, your request for an appointment at: {appointment.start_time} ,{appointment.appointment_date}
        is was approved.
        '''
        email_message_therapist = f'''
        you approved an appointment for: {appointment.user} {request.user.last_name}, at: {appointment.start_time} ,{appointment.appointment_date}
        '''
        message_to_user = EmailMessage(
            'Appointment Request',
            email_message_user,
            therapist_email,
            [appointment.user.user.email],
        )

        message_to_therapist = EmailMessage(
            'Your appointment',
            email_message_therapist,
            therapist_email,
            [therapist_email],
            reply_to=[appointment.user.user.email],
        )
        message_to_user.send()
        message_to_therapist.send()
    else:
        appointment.choice = 'P'
        return redirect('appointment_response', pk)
    return redirect('home')
