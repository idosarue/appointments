from django.db import models
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from patient.models import Appointment, AppointmentResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage
from patient.forms import  AppointmentResponseForm
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from accounts.forms import ValidationForm

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class AppointmentListView(SuperUserRequiredMixin, ListView):
    model = Appointment
    template_name = 'therapist/apt_requests.html'
    context_object_name = 'appointments'
    ordering = 'timestamp'

class AcceptedAppointmentListView(SuperUserRequiredMixin, ListView):
    model = Appointment
    template_name = 'therapist/accepted_apt.html'
    ordering = 'timestamp'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(is_approved=True)
        context['appointments_response'] = AppointmentResponse.objects.filter(is_approved=True)
        return context

class PendingAppointmentListView(SuperUserRequiredMixin, ListView):
    model = AppointmentResponse
    template_name = 'therapist/pending_apts.html'
    context_object_name = 'appointments'



class AppointmentResponseView(LoginRequiredMixin, CreateView):
    form_class = AppointmentResponseForm
    template_name = 'patient/appointment_response.html'
    success_url = reverse_lazy('home')
    
    def get_appointment(self):
        appoint_id = self.kwargs['pk']
        return get_object_or_404(Appointment, id=appoint_id)

    def form_valid(self, form):
        appoint = form.save(commit=False)
        appoint.original_request = self.get_appointment()
        appoint.user = appoint.original_request.user
        appoint.save()
        therapist_email = 'testdjangosar@gmail.com'

        email_message_user = f'''
        Hello {appoint.original_request.user.user.username}, your request for an appointment at: {appoint.original_request.start_time} , {appoint.original_request.appointment_date}
        is not available, are you free at {appoint.start_time}, {appoint.appointment_date} ?
        '''
        # message_to_user = EmailMessage(
        #     'Appointment Request',
        #     email_message_user,
        #     therapist_email,
        #     [appoint.original_request.user.user.email],
        #     reply_to=[therapist_email],
        # )
        send_mail(
            'Appointment Request',
            'tests',
            therapist_email,
            [appoint.original_request.user.user.email],
            fail_silently=False,
            html_message= render_to_string('therapist/email.html', {'appointment': appoint, 'user': appoint.original_request.user.user})
            )
        
        # message_to_user.send()
        return super().form_valid(form)


@login_required
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
        appointment.save()
        return redirect('appointment_response', pk)
    return redirect('home')

@login_required
def update_appointment_response_status(request, pk, status):
    appointment = get_object_or_404(AppointmentResponse, id=pk)
    if request.user.profile == appointment.original_request.user:
        if status == 'accept':
            print(request.user.profile)
            print(appointment.id)
            appointment.is_approved = True
            appointment.save()
        else:
            return redirect('query_appointment')
    return redirect('home')

class AppointmentUpdateView(SuperUserRequiredMixin, UpdateView):
    model = AppointmentResponse
    fields = ['start_time', 'appointment_date']

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk':self.object.id})

