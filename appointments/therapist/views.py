from django.core.paginator import Paginator
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse_lazy
from django.utils import html
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django_filters.views import FilterView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from patient.models import Appointment, AppointmentResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import date, datetime, time, timedelta
import datetime as dt
import numpy as np
from itertools import chain
from therapist.my_calendar import Calendar
from django.http import JsonResponse
import json
from django.utils.safestring import mark_safe
from .models import Comment, Day, WorkingTime, Date
from send_emails import (send_response_email_to_user, 
send_success_message_email_to_user, 
send_success_message_email_to_therapist, 
send_success_repsponse_message_email_to_therapist)
from django.core import mail
from .forms import(
     DisabledDatesForm, 
     EditAppointmentForm, 
     EditAppointmentResponseForm, 
     AppointmentResponseForm, 
     CalendarForm, 
     TherapistCreateAppointmentForm, 
     WorkingTimeForm,
     AppointmentFilter,
     PendingAppointmentFilter,
     CreateCommentForm,
     EditCommentForm
     )



def error_404(request, exception):
        data = {}
        return render(request, 'patient/home.html', data)

def error_403(request, exception):
        data = {}
        return render(request, 'patient/home.html', data)

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
        users = Profile.objects.filter(user__is_superuser=False)
        pag = Paginator(users,10)
        page_number = self.request.GET.get('page')
        page_obj = pag.get_page(page_number) 
        context['user_list'] = users
        context['page_obj'] = page_obj
        return context

class AppointmentListView(SuperUserRequiredMixin, ListView):
    model = Appointment
    template_name = 'therapist/apt_requests.html'
    ordering = 'timestamp'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(choice=None)
        return context

class AppointmentResponseView(SuperUserRequiredMixin, CreateView):
    form_class = AppointmentResponseForm
    template_name = 'patient/appointment_response.html'
    success_url = reverse_lazy('home')
    
    def form_invalid(self, form):
        return JsonResponse({"error": form.errors}, status=400)
    
    def get_appointment(self):
        appoint_id = self.kwargs['pk']
        return get_object_or_404(Appointment, id=appoint_id)

    def form_valid(self, form):
        start_time = form.cleaned_data['start_time']
        appointment_date = form.cleaned_data['appointment_date']
        start = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = time(hour = start.hour + 1, minute=start.minute)
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
        appoint.end_time = end_time
        appoint.week_day = Day.objects.get(week_day=appoint.appointment_date.weekday())

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
    end_time = time(hour = start_time.hour + 1, minute=start_time.minute)
    if status == 'accept':
        if AppointmentResponse.is_vacant(start_time, appointment_date, end_time) and Appointment.is_vacant(start_time, appointment_date, end_time):
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
        context['past_appointments'] = past_appointments
        context['future_appointments'] = future_appointments
        context['past_appointments_response'] = past_appointments_response
        context['future_appointments_response'] = future_appointments_response
        return context


def get_date_f(request, year, month, day):
    print(date(year, month, day))
    return date(year, month, day)

class CalendarView(SuperUserRequiredMixin,FormView):
    model = Appointment
    template_name = 'therapist/newcal.html'
    form_class = CalendarForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CalendarForm(self.request.GET)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
        else:
            year = year=datetime.now().year
            month = datetime.now().month
        if not year and not month:
            cal = Calendar(year=datetime.now().year or year, month=datetime.now().month or month)
        else:
            cal = Calendar(year=int(year), month=int(month))

        cal.setfirstweekday(6)
        html_cal = cal.formatmonth(withyear=True)
        context['form'] = CalendarForm(self.request.GET or None)
        context['edit_appoint_form'] = EditAppointmentForm()
        context['edit_response_form'] = EditAppointmentResponseForm()
        context['comment_form'] = CreateCommentForm()
        context['edit_comment_form'] = EditCommentForm()
        context['appoint_form'] = TherapistCreateAppointmentForm()
        context['calendar'] = html_cal

        return context

class AppointmentUpdateView(SuperUserRequiredMixin, UpdateView):
    success_url = reverse_lazy('calendar')
    form_class = EditAppointmentForm
    template_name = 'therapist/edit_appoint.html'
    model = Appointment

    def form_invalid(self, form):
        return JsonResponse({"error": form.errors}, status=400)


    def get_appoint(self):
        appoint_id = self.kwargs['pk']
        appoint = get_object_or_404(Appointment, id=appoint_id)
        return appoint
    
    def form_valid(self, form):
        start_time = form.cleaned_data['start_time']
        appointment_date = form.cleaned_data['appointment_date']
        start = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = time(hour = start.hour + 1, minute=start.minute)        
        appoint = form.save(commit=False)
        x = datetime(
            appoint.appointment_date.year,
            appoint.appointment_date.month,
            appoint.appointment_date.day,
            appoint.start_time.hour,
            appoint.start_time.minute,
            )
        appoint.date_t = x
        appoint.end_time = end_time
        appoint.week_day = Day.objects.get(week_day=appoint.appointment_date.weekday())

        appoint.save()
        appointment = self.get_appoint()
        print(appointment.start_time)
        send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date)
        return super().form_valid(form)

class AppointmentResponseUpdateView(SuperUserRequiredMixin, UpdateView):
    success_url = reverse_lazy('calendar')
    template_name = 'therapist/edit_appoint.html'
    form_class = EditAppointmentResponseForm
    model = AppointmentResponse

    def form_invalid(self, form):
        return JsonResponse({"error": form.errors}, status=400)

    def get_appoint(self):
        appoint_id = self.kwargs['pk']
        appoint = get_object_or_404(AppointmentResponse, id=appoint_id)
        return appoint

    def form_valid(self, form):
        start_time = form.cleaned_data['start_time']
        appointment_date = form.cleaned_data['appointment_date']
        start = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = time(hour = start.hour + 1, minute=start.minute)
        if not Appointment.is_vacant(start_time, appointment_date, end_time) or not AppointmentResponse.is_vacant(start_time, appointment_date, end_time):
            messages.error(self.request, 'no available meetings for that date or time, please choose another date or time')
            return super().form_invalid(form)
        appoint = form.save(commit=False)
        x = datetime(
            appoint.appointment_date.year,
            appoint.appointment_date.month,
            appoint.appointment_date.day,
            appoint.start_time.hour,
            appoint.start_time.minute,
            )
        appoint.date_t = x
        appoint.end_time = end_time
        appoint.week_day = Day.objects.get(week_day=appoint.appointment_date.weekday())
        appointment = self.get_appoint()
        send_success_message_email_to_user(appointment.user.user, appointment.start_time, appointment.appointment_date)
        return super().form_valid(form)


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

    # def get_date(self):
    #     year = self.kwargs['year']
    #     month = self.kwargs['month']
    #     day = self.kwargs['day']
    #     print(year, month, day)
    #     appoint_date = dt.date(year, month, day)
    #     return appoint_date

    def form_invalid(self, form):
        return JsonResponse({"error": form.errors}, status=400)

    def form_valid(self, form):
        start_time = form.cleaned_data['start_time']
        appointment_date = form.cleaned_data['appointment_date']
        start = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = time(hour = start.hour + 1, minute=start.minute)
        response_data = {}
        appoint = form.save(commit=False)
        appoint.user = form.cleaned_data['user']
        appoint.choice = 'A'
        appoint.appointment_date = appointment_date
        appoint.is_approved=True
        appoint.end_time = end_time
        x = datetime(
            appoint.appointment_date.year,
            appoint.appointment_date.month,
            appoint.appointment_date.day,
            appoint.start_time.hour,
            appoint.start_time.minute,
            )
        appoint.date_t = x
        appoint.end_time = end_time
        appoint.week_day = Day.objects.get(week_day=appoint.appointment_date.weekday())
        appoint.save()
        send_success_message_email_to_user(appoint.user.user, appoint.start_time, appoint.appointment_date)
        send_success_message_email_to_therapist(appoint.user.user, appoint.start_time, appoint.appointment_date)
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['user'].queryset = Profile.objects.exclude(id=1)
        # form.fields['appointment_date'].initial = self.get_date()
        return form
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['date'] = self.get_date()
    #     return context


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


class WorkingTimeView(SuperUserRequiredMixin,UpdateView):
    form_class = WorkingTimeForm
    template_name = 'therapist/preferences/working_time.html'
    success_url = reverse_lazy('preferences')
    model = WorkingTime

    def get_object(self, queryset=None):
        a = WorkingTime.objects.first()
        return a

class PreferencesView(SuperUserRequiredMixin, ListView):
    model = Day
    template_name = 'therapist/preferences/therapist_settings.html'
    context_object_name = 'days'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_time = WorkingTime.objects.first().start_time
        last_appoint_time = WorkingTime.create_time_choice()[-1][0]
        c = datetime.combine(date.today(), time(hour = last_appoint_time.hour, minute=last_appoint_time.minute)) + timedelta(hours=1)
        y = c.time()
        message = f'based on time specified your last appointment will end at {y}'
        context['start_time'] = start_time
        context['end_time'] = y
        context['message'] = message
        context['disabled_dates'] = Date.objects.filter(is_disabled=True)
        context['working_form'] = WorkingTimeForm(instance=WorkingTime.objects.first())
        context['date_form'] = DisabledDatesForm()
        return context

class DisableDatesView(SuperUserRequiredMixin,CreateView):
    form_class = DisabledDatesForm
    template_name = 'therapist/preferences/disable_dates.html'
    success_url = reverse_lazy('preferences')

    def form_valid(self, form):
        date = form.save(commit=False)
        date.is_disabled = True
        date.save()
        return super().form_valid(form)


@user_passes_test(lambda u: u.is_superuser)
def enable_date(request, pk):
    date = get_object_or_404(Date, id=pk)
    date.is_disabled = False
    date.save()
    return redirect('preferences')



class AppointsView(SuperUserRequiredMixin,FilterView):
    template_name = 'therapist/accepted_appointments.html'
    model = Appointment

    def get_multiple(self):
        # if not 'appointment_date' in self.request.GET:
        #     self.request.GET.update({'appointment_date':date.today()})
        #     # filter = AppointmentFilter(self.request.GET, queryset=Appointment.display(appointment_date=date.today()))
        #     # filter2 = AppointmentFilter(self.request.GET, queryset=AppointmentResponse.display(appointment_date=date.today()))
        filter = AppointmentFilter(self.request.GET, queryset=Appointment.display())
        filter2 = AppointmentFilter(self.request.GET, queryset=AppointmentResponse.display())
        return {'filter':filter, 'filter2':filter2}

    def get_context_data(self, **kwargs):
        filter = AppointmentFilter(self.request.GET, queryset=Appointment.display())
        filter2 = AppointmentFilter(self.request.GET, queryset=AppointmentResponse.display())
        x = sorted(list(chain(filter.qs, filter2.qs)), key=lambda x: x.appointment_date)
        pag = Paginator(x,10)
        page_number = self.request.GET.get('page')
        page_obj = pag.get_page(page_number) 
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        context['filter'] = filter
        context['filter2'] = filter2
        # context['today'] = date.today()
        return context

class PendingAppointsView(SuperUserRequiredMixin,FilterView):
    template_name = 'therapist/pending_apts.html'
    model = AppointmentResponse

    def get_context_data(self, **kwargs):
        filter = PendingAppointmentFilter(self.request.GET, queryset=AppointmentResponse.objects.filter(choice='P', is_cancelled=False, is_approved=False))
        pag = Paginator(filter.qs,10)
        page_number = self.request.GET.get('page')
        page_obj = pag.get_page(page_number) 
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        context['filter'] = filter
        return context

class AppointsRequestsView(SuperUserRequiredMixin,FilterView):
    template_name = 'therapist/apt_requests.html'
    model = Appointment

    def get_context_data(self, **kwargs):
        filter = PendingAppointmentFilter(self.request.GET, queryset=Appointment.objects.filter(choice=None, is_cancelled=False, is_approved=False))
        pag = Paginator(filter.qs,10)
        page_number = self.request.GET.get('page')
        page_obj = pag.get_page(page_number) 
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        context['filter'] = filter
        return context

class CreateCommentView(SuperUserRequiredMixin, CreateView):
    form_class = CreateCommentForm
    template_name = 'therapist/create_comment.html'
    success_url = reverse_lazy('calendar')

    def form_invalid(self, form):
        return JsonResponse({"error": form.errors}, status=400)


class EditCommentView(SuperUserRequiredMixin, UpdateView):
    template_name = 'therapist/create_comment.html'
    success_url = reverse_lazy('calendar')
    form_class = EditCommentForm

    def form_invalid(self, form):
        return JsonResponse({"error": form.errors}, status=400)


    def get_object(self, queryset=None):
        comment_id = self.kwargs['pk']
        return get_object_or_404(Comment, id=comment_id)
   

@user_passes_test(lambda u: u.is_superuser)
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.is_deleted = True
    comment.save()
    return redirect('calendar')