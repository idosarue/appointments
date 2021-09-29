from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from patient.models import Appointment, AppointmentResponse,ContactUsersMessagesToTherapist
from accounts.models import Profile
from django.db import models
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from .forms import AppointmentForm, UserAppointmentFilter, ContactFormEmailPatient
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, time, date 
from django_filters.views import FilterView
from itertools import chain
from therapist.models import Day
from django.core.paginator import Paginator
from send_emails import (send_message_to_therapist, 
send_message_to_user, 
send_message_to_therapist_after_update, send_contact_message_to_therapist)

# Create your views here.
def home(request):
    return render(request, 'patient/home.html')

class CreateContactMessageToTherapist(CreateView):
    model = ContactUsersMessagesToTherapist
    form_class = ContactFormEmailPatient
    template_name = 'patient/home.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        send_contact_message_to_therapist(form.cleaned_data['email'], form.cleaned_data['subject'], form.cleaned_data['message'])
        return super().form_valid(form)

class CreateAppointmentView(LoginRequiredMixin, CreateView):
    form_class = AppointmentForm
    template_name = 'patient/query_appointment.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        start_time = form.cleaned_data['start_time']
        appointment_date = form.cleaned_data['appointment_date']
        start = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = time(hour = start.hour + 1, minute=start.minute)
        appoint = form.save(commit=False)
        appoint.user = self.request.user.profile
        x = datetime(
            appoint.appointment_date.year,
            appoint.appointment_date.month,
            appoint.appointment_date.day,
            appoint.start_time.hour,
            appoint.start_time.minute,
            )
        appoint.end_time = end_time
        appoint.date_t = x
        appoint.week_day = Day.objects.get(week_day=appoint.appointment_date.weekday())
        appoint.save()
        send_message_to_user(self.request.user, start_time, appointment_date)
        send_message_to_therapist(self.request.user, start_time, appointment_date)
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
    

class AppointsListView(LoginRequiredMixin,FilterView):
    template_name = 'patient/appointments.html'
    model = Appointment

    # def get_multiple(self):
    #     # if not 'appointment_date' in self.request.GET:
    #     #     self.request.GET.update({'appointment_date':date.today()})
    #     #     # filter = AppointmentFilter(self.request.GET, queryset=Appointment.display(appointment_date=date.today()))
    #     #     # filter2 = AppointmentFilter(self.request.GET, queryset=AppointmentResponse.display(appointment_date=date.today()))
    #     filter = UserAppointmentFilter(self.request.GET, queryset=Appointment.display())
    #     filter2 = UserAppointmentFilter(self.request.GET, queryset=AppointmentResponse.display())
    #     return {'filter':filter, 'filter2':filter2}

    def get_context_data(self, **kwargs):
        filter = UserAppointmentFilter(self.request.GET, queryset=Appointment.display(user=self.request.user.profile))
        filter2 = UserAppointmentFilter(self.request.GET, queryset=AppointmentResponse.display(user=self.request.user.profile))
        x = sorted(list(chain(filter.qs, filter2.qs)), key=lambda x: x.appointment_date)
        pag = Paginator(x,10)
        page_number = self.request.GET.get('page')
        page_obj = pag.get_page(page_number) 
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        context['filter'] = filter
        context['filter2'] = filter2
        context['today'] = date.today()
        return context


    
