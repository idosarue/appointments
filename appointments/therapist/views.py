from django.db.models import query
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from patient.models import Appointment, AppointmentResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.contrib.auth.models import User
from datetime import datetime
import datetime as dt
from therapist.my_calendar import Calendar
from django.utils.safestring import mark_safe
from .models import Day, WorkingTime, Date
from send_emails import (send_response_email_to_user, 
send_success_message_email_to_user, 
send_success_message_email_to_therapist, 
send_success_repsponse_message_email_to_therapist)
from .forms import(
     DisabledDatesForm, 
     EditAppointmentForm, 
     EditAppointmentResponseForm, 
     AppointmentResponseForm, 
     CalendarForm, 
     TherapistCreateAppointmentForm, 
     WorkingTimeForm
     )


class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_superuser
        else:
            return False 

class AllUsersList(SuperUserRequiredMixin, ListView):
    model = Profile
    template_name = 'therapist/all_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.filter(is_superuser=False)
        context['user_list'] = [user.profile for user in users]
        return context

class AppointmentListView(SuperUserRequiredMixin, ListView):
    model = Appointment
    template_name = 'therapist/apt_requests.html'
    ordering = 'timestamp'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(choice=None)
        return context

class AcceptedAppointmentListView(SuperUserRequiredMixin, ListView):
    model = Appointment
    template_name = 'therapist/accepted_apt.html'
    ordering = 'timestamp'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appoints_display = Appointment.display()
        appoints_res_display = AppointmentResponse.display()
        if appoints_display:
            context['appointments'] = appoints_display
        if appoints_res_display:
            context['appointments_response'] = appoints_res_display
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
        if not Appointment.is_vacant(start_time=form.cleaned_data['start_time'], appointment_date=form.cleaned_data['appointment_date']) or not AppointmentResponse.is_vacant(start_time=form.cleaned_data['start_time'], appointment_date=form.cleaned_data['appointment_date']):
            messages.error(self.request, 'no available meetings for that date or time, please choose another date or time')
            return super().form_invalid(form)
        appoint = form.save(commit=False)
        appoint.original_request = self.get_appointment()
        appoint.user = appoint.original_request.user
        appoint.choice = 'P'
        appoint.original_request.choice = 'R'
        appoint.original_request.is_cancelled = True
        appoint.original_request.save()
        x = datetime(
            appoint.appointment_date.year,
            appoint.appointment_date.month,
            appoint.appointment_date.day,
            appoint.start_time.hour,
            appoint.start_time.minute,
            )
        appoint.date_t = x
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
        if AppointmentResponse.is_vacant(start_time, appointment_date) and Appointment.is_vacant(start_time, appointment_date):
            appointment.choice = 'A'
            appointment.is_approved = True
            appointment.save()
            send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date)
            send_success_message_email_to_therapist(appointment.user.user, appointment.start_time, appointment.appointment_date)
        else:
            messages.error(request, 'you cannot have meetings on the same time, or set meetings for times pending, send the user an update request')
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
            messages.success(request, 'appointment approved')
        else:
            return redirect('query_appointment_update', pk)
    return redirect('profile')



class UserAppointments(SuperUserRequiredMixin, ListView):
    model = Profile
    template_name = 'therapist/user_appointments.html'

    def get_profile(self):
        profile_id = self.kwargs['pk']
        return get_object_or_404(Profile, id=profile_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        past_appointments = Appointment.display(user=self.get_profile(), date_t__lt=datetime.today())
        future_appointments = Appointment.display(user=self.get_profile(), date_t__gt=datetime.today())
        past_appointments_response =  AppointmentResponse.display(user=self.get_profile(), date_t__lt=datetime.today())
        future_appointments_response = AppointmentResponse.display(user=self.get_profile(), date_t__gt=datetime.today())
        if past_appointments:
            context['past_appointments'] = past_appointments
        if future_appointments:
            context['future_appointments'] = future_appointments
        if past_appointments_response :
            context['past_appointments_response'] = past_appointments_response
        if future_appointments_response:
            context['future_appointments_response'] = AppointmentResponse.display(user=self.get_profile(), date_t__gt=datetime.today())
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
        cal.setfirstweekday(6)
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
        if not Appointment.is_vacant(start_time=form.cleaned_data['start_time'], appointment_date=form.cleaned_data['appointment_date']) or not AppointmentResponse.is_vacant(start_time=form.cleaned_data['start_time'], appointment_date=form.cleaned_data['appointment_date']):
            messages.error(self.request, 'no available meetings for that date or time, please choose another date or time')
            return super().form_invalid(form)
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
        if not Appointment.is_vacant(start_time=form.cleaned_data['start_time'], appointment_date=form.cleaned_data['appointment_date']) or not AppointmentResponse.is_vacant(start_time=form.cleaned_data['start_time'], appointment_date=form.cleaned_data['appointment_date']):
            messages.error(self.request, 'no available meetings for that date or time, please choose another date or time')
            print('not')
            return super().form_invalid(form)
        form.save()
        appointment = self.get_appoint()
        send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date)
        return super().form_valid(form)

# @user_passes_test(lambda u: u.is_superuser)
# def confirm_delete_appointment(request, pk):
#     if status == 'yes':
#         return redirect('delete_appointment', pk)
#     return render(request, 'therapist/confirm_delete.html')

@user_passes_test(lambda u: u.is_superuser)
def delete_appointment(request, pk):
    appoint = get_object_or_404(Appointment, id=pk)
    appoint.is_cancelled = True
    appoint.save()
    return redirect('calendar')

@user_passes_test(lambda u: u.is_superuser) 
def delete_appointment_response(request, pk):
    appoint = get_object_or_404(AppointmentResponse, id=pk)
    appoint.is_cancelled = True
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
        appoint_date = dt.date(year, month, day)
        return appoint_date


    def form_valid(self, form):
        if not Appointment.is_vacant(start_time=form.cleaned_data['start_time'], appointment_date=form.cleaned_data['appointment_date']) or not AppointmentResponse.is_vacant(start_time=form.cleaned_data['start_time'], appointment_date=form.cleaned_data['appointment_date']):
            messages.error(self.request, 'no available meetings for that date or time, please choose another date or time')
            return super().form_invalid(form)
        appoint = form.save(commit=False)
        appoint.user = form.cleaned_data['user']
        appoint.choice = 'A'
        appoint.appointment_date = form.cleaned_data['appointment_date']
        appoint.is_approved=True
        # appoint.end_time = dt.time(hour=appoint.start_time.hour +1, minute=appoint.start_time.minute)
        print(appoint.start_time)
        appoint.save()
        send_success_message_email_to_user(appoint.user.user, appoint.start_time, appoint.appointment_date)
        send_success_message_email_to_therapist(appoint.user.user, appoint.start_time, appoint.appointment_date)
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['user'].queryset = Profile.objects.exclude(id=1)
        form.fields['appointment_date'].initial = self.get_date()
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = self.get_date()
        return context


@user_passes_test(lambda u: u.is_superuser)
def disable_day(request, pk):
    day = get_object_or_404(Day, id=pk)
    print(day.week_day)
    if not Appointment.can_disable(day.week_day) or not AppointmentResponse.can_disable(day.week_day):
        messages.error(request, 'you have meetings or pending meetings on that day please make sure that weekday is clear before disabling')
        return redirect('preferences')
    else:
        day.is_disabled = True
        day.save()
    return redirect('preferences')

@user_passes_test(lambda u: u.is_superuser)
def enable_day(request, pk):
    day = get_object_or_404(Day, id=pk)
    day.is_disabled = False
    day.save()
    return redirect('preferences')
# create_appoint/<int:year>/<int:month>/<int:day>/
# @user_passes_test(lambda u: u.is_superuser)
# def disable_date(request, year, month, day):
#     date = dt.date(year, month, day)
#     Date.objects.create(date=date, is_disabled=True)
#     return redirect('calendar')

class WorkingTimeView(SuperUserRequiredMixin,UpdateView):
    form_class = WorkingTimeForm
    template_name = 'therapist/working_time.html'
    success_url = reverse_lazy('preferences')
    model = WorkingTime

    def get_object(self, queryset=None):
        a = WorkingTime.objects.first()
        return a


class PreferencesView(SuperUserRequiredMixin, ListView):
    model = Day
    template_name = 'therapist/therapist_settings.html'
    context_object_name = 'days'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_time = WorkingTime.objects.first().start_time
        end_time = WorkingTime.objects.first().end_time
        minutes = WorkingTime.objects.first().minutes
        context['start_time'] = dt.time(hour=start_time, minute=minutes)
        context['end_time'] = dt.time(hour=end_time, minute=minutes)
        return context
    
class DisableDatesView(SuperUserRequiredMixin,CreateView):
    form_class = DisabledDatesForm
    template_name = 'therapist/disable_dates.html'
    success_url = reverse_lazy('preferences')

    def form_valid(self, form):
        date = form.save(commit=False)
        date.is_disabled = True
        date.save()
        return super().form_valid(form)