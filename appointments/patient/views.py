from patient.models import Appointment
from accounts.models import Profile
from django.db import models
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from .forms import AppointmentForm, AppointmentResponseForm
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage

# Create your views here.
def home(request):
    return render(request, 'patient/home.html')


class CreateAppointmentView(CreateView):
    form_class = AppointmentForm
    template_name = 'patient/query_appointment.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        appoint = form.save(commit=False)
        appoint.user = self.request.user.profile
        appoint.save()
        email_message_user = f'''
        Hello {self.request.user.username}, your request for an appointment at: {form.cleaned_data['start_time']} , {form.cleaned_data['appointment_date']}
        is being reviewed, we will get back to you soon.
        '''
        email_message_therapist = f'''
        {self.request.user.first_name} {self.request.user.last_name}, requested an appointment at: {form.cleaned_data['start_time']} , {form.cleaned_data['appointment_date']}
        '''
        message_to_user = EmailMessage(
            'Appointment Request',
            email_message_user,
            'testdjangosar@gmail.com',
            [self.request.user.email],
        )

        message_to_therapist = EmailMessage(
            'Your appointment',
            email_message_therapist,
            'testdjangosar@gmail.com',
            ['testdjangosar@gmail.com'],
            reply_to=[self.request.user.email],
        )
        message_to_user.send()
        message_to_therapist.send()
        return super().form_valid(form)


class AppointmentResponseView(CreateView):
    form_class = AppointmentResponseForm
    template_name = 'patient/appointment_response.html'
    success_url = reverse_lazy('home')
    
    def get_appointment(self):
        appoint_id = self.kwargs['pk']
        return get_object_or_404(Appointment, id=appoint_id)

    def form_valid(self, form):
        appoint = form.save(commit=False)
        appoint.original_response = self.get_appointment()
        appoint.save()
        therapist_email = 'testdjangosar@gmail.com'
        email_message_user = f'''
        Hello {self.request.user.username}, your request for an appointment at: {appoint.original_response.start_time} , {appoint.original_response.appointment_date}
        is not available, are you free at {appoint.start_time}, {appoint.appointment_date} ?
        '''
        message_to_user = EmailMessage(
            'Appointment Request',
            email_message_user,
            'testdjangosar@gmail.com',
            [appoint.original_response.user.user.email],
            reply_to=[therapist_email],
        )

        message_to_user.send()
        return super().form_valid(form)