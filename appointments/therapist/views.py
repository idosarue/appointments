from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from patient.models import Appointment, AppointmentResponse
from django.contrib.auth.decorators import user_passes_test
from .forms import EditAppointmentForm, EditAppointmentResponseForm, AppointmentResponseForm
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from datetime import datetime, date
from django.contrib.auth.models import User
from .utils import Calendar
from django.utils.safestring import mark_safe
from .forms import CalendarForm, TherapistCreateAppointmentForm
from send_emails import (send_response_email_to_user, 
send_success_message_email_to_user, 
send_success_message_email_to_therapist, 
send_success_repsponse_message_email_to_therapist)

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_superuser 

class AllUsersList(SuperUserRequiredMixin, ListView):
    model = Profile
    template_name = 'therapist/all_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(is_superuser = True)
        context['user_list'] = Profile.objects.exclude(user= user)
        return context

class AppointmentListView(SuperUserRequiredMixin, ListView):
    model = Appointment
    template_name = 'therapist/apt_requests.html'
    ordering = 'timestamp'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(is_approved=False, choice=None)
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = AppointmentResponse.objects.exclude(is_approved=True)
        return context

class AppointmentResponseView(SuperUserRequiredMixin, CreateView):
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
        appoint.choice = 'P'
        appoint.original_request.choice = 'R'
        appoint.original_request.save()
        appoint.save()
        send_response_email_to_user(appoint.original_request.user.user, appoint)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.get_appointment()
        return context

@user_passes_test(lambda u: u.is_superuser)
def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment_date = appointment.appointment_date
    start_time = appointment.start_time
    if status == 'accept':
        if not AppointmentResponse.objects.filter(start_time=start_time,appointment_date=appointment_date, choice='P').exists():
            if not Appointment.objects.filter(start_time=start_time,appointment_date=appointment_date, is_approved=True).exists():
                appointment.choice = 'A'
                appointment.is_approved = True
                appointment.save()
                send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date)
                send_success_message_email_to_therapist(appointment.user.user, appointment.start_time, appointment.appointment_date)
            else:
                messages.error(request, 'you cannot have meetings on the same time, send the user an update request')
                return redirect('appointment_response', pk)
        else:
            messages.error(request, 'you already have a pending meeting on the same time, send the user an update request')
            return redirect('appointment_response', pk)
    else:
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
            send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date)
            send_success_repsponse_message_email_to_therapist(appointment.user.user, appointment.start_time, appointment.appointment_date)
        else:
            return redirect('query_appointment_update', pk)
    return redirect('home')



class UserAppointments(SuperUserRequiredMixin, ListView):
    model = Profile
    template_name = 'therapist/user_appointments.html'

    def get_profile(self):
        profile_id = self.kwargs['pk']
        return get_object_or_404(Profile, id=profile_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['past_appointments'] = self.get_profile().appointment_set.filter(appointment_date__lt=datetime.today(), is_approved=True)
        context['future_appointments'] = self.get_profile().appointment_set.filter(appointment_date__gte=datetime.today(),is_approved=True)
        context['future_appointments_response'] = self.get_profile().appointmentresponse_set.filter(appointment_date__gte=datetime.today(),is_approved=True)
        context['past_appointments_response'] = self.get_profile().appointmentresponse_set.filter(appointment_date__lt=datetime.today(), is_approved=True)
        return context

class CalendarView(SuperUserRequiredMixin,ListView):
    model = Appointment
    template_name = 'therapist/calendar.html'

    def get_date(self):
        form = CalendarForm(self.request.GET)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            print(year)
            return {'year' : year, 'month' : month}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.get_date():
            cal = Calendar(year=datetime.now().year, month=datetime.now().month)
        else:
            year = self.get_date()['year']
            month = self.get_date()['month']
            cal = Calendar(year=int(year), month=int(month))
        html_cal = cal.formatmonth(withyear=True)
        context['form'] = CalendarForm
        context['calendar'] = mark_safe(html_cal)
        return context


class AppointmentUpdateView(SuperUserRequiredMixin, UpdateView):
    success_url = reverse_lazy('calendar')
    form_class = EditAppointmentForm
    template_name = 'therapist/edit_appoint.html'
    model = Appointment

    def get_appoint(self):
        appoint_id = self.kwargs['pk']
        appoint = get_object_or_404(Appointment, id=appoint_id)
        return appoint
    
    def form_valid(self, form):
        form.save()
        appointment = self.get_appoint()
        print(appointment.start_time)
        send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date)
        return super().form_valid(form)

class AppointmentResponseUpdateView(SuperUserRequiredMixin, UpdateView):
    success_url = reverse_lazy('calendar')
    template_name = 'therapist/edit_appoint.html'
    form_class = EditAppointmentResponseForm
    model = AppointmentResponse

    def get_appoint(self):
        appoint_id = self.kwargs['pk']
        appoint = get_object_or_404(AppointmentResponse, id=appoint_id)
        return appoint

    def form_valid(self, form):
        form.save()
        appointment = self.get_appoint()
        send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date)
        return super().form_valid(form)

@user_passes_test(lambda u: u.is_superuser)
def delete_appointment(request, pk):
    appoint = get_object_or_404(Appointment, id=pk)
    appoint.is_approved = False
    appoint.save()
    return redirect('calendar')

@user_passes_test(lambda u: u.is_superuser) 
def delete_appointment_response(request, pk):
    appoint = get_object_or_404(AppointmentResponse, id=pk)
    appoint.is_approved = False
    appoint.save()
    return redirect('calendar')

class TherapistCreateAppointmentView(LoginRequiredMixin, CreateView):
    form_class = TherapistCreateAppointmentForm
    template_name = 'therapist/create_appoint.html'
    success_url = reverse_lazy('calendar')

    def get_date(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        print(year, month, day)
        appoint_date = date(year, month, day)
        return appoint_date

    def form_valid(self, form):
        appoint = form.save(commit=False)
        print(self.get_date())
        appoint.user = form.cleaned_data['user']
        appoint.choice = 'A'
        appoint.appointment_date = self.get_date()
        appoint.is_approved=True
        appoint.save()
        send_success_message_email_to_user(appoint.user.user, appoint.start_time, appoint.appointment_date)
        send_success_message_email_to_therapist(appoint.user.user, appoint.start_time, appoint.appointment_date)
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['user'].queryset = Profile.objects.exclude(id=1)
        form.fields['appointment_date'].value = date(2021, 1, 1)
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = self.get_date()
        return context