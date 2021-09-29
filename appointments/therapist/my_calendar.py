from datetime import date, datetime, timedelta
from calendar import HTMLCalendar, month_name
from patient.models import Appointment, AppointmentResponse
from therapist.models import Date, Day, Comment
from django.urls import reverse_lazy
import holidays
from therapist.forms import CreateCommentForm
from django.template.loader import render_to_string
from django.template.context_processors import csrf
from itertools import chain

class Calendar(HTMLCalendar):
    def __init__(self, year, month):
        self.year = year
        self.month = month
        super(Calendar).__init__()

    def formatday(self, day, events, events2, comments):
        events_per_day = events.filter(appointment_date__day=day).order_by('start_time')
        events_per_day2 = events2.filter(appointment_date__day=day).order_by('start_time')
        comments = comments.filter(date__day=day)
        # d = ''
        appointments = []
        appointments_response = []
        y = []

        for event in events_per_day:
            # d += f'<li id="{event.id}"> {event.start_time} {event.user.user.first_name} {event.user.user.last_name} {event.user.phone_number} <a  href="{reverse_lazy("update_apt", kwargs={"pk":event.id})}">edit</a> <br> <a href="{reverse_lazy("delete_appointment", kwargs= {"pk" :event.id})}" class="confirm_delete">Cancel</a></li>'
            appointments.append(event)
        for event in events_per_day2:
            # d += f'<li id="{event.id}"> {event.start_time} {event.user.user.first_name} {event.user.user.last_name} {event.user.phone_number} <a href="{reverse_lazy("update_apt_res", kwargs={"pk":event.id})}">edit</a> <br><a href="{reverse_lazy("delete_appointment_response", kwargs= {"pk" :event.id})}" class="confirm_delete">Cancel</a></li>'
            appointments_response.append(event)
        
        x = sorted(list(chain(appointments, appointments_response)), key=lambda x: x.start_time)
        print(x)

        if day:
            disabled = False
            v_date = date(self.year, self.month, day)
            isr_holidays = holidays.CountryHoliday('ISR')
            holi = ''
            # link = f"<a href='{reverse_lazy('create_comment', kwargs={'year': self.year, 'month': self.month, 'day': day})}'>add comment</a>"
            if v_date in isr_holidays:
                holi += isr_holidays.get(f'{v_date.year}-{v_date.month}-{v_date.day}')
            if (v_date.weekday() in Day.disabled_days() or v_date in Date.disabled_dates()):
                disabled = True
            # if v_date > date.today() and not v_date.weekday() in Day.disabled_days() and not v_date in Date.disabled_dates():
            #     create_appoint_a = f"<a href='{reverse_lazy('create_appoint', kwargs={'year': self.year, 'month': self.month, 'day': day})}'>+</a>"
            else:
                create_appoint_a = ''
            for comment in comments:
                y.append(comment)
            day_dic = {'day_num': day,'sorted_appoints':x ,'appointments': appointments, 'appointments_response':appointments_response, 'disabled':disabled, 'year':int(self.year), 'month':self.month, 'comments':y, 'holiday':holi}
            return day_dic

        
        return '<td></td>'


    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]     
        return {'name':s, 'year':theyear, 'month_num':themonth}


    def formatweek(self, theweek, events, events2, comments):
        week = []
        for d, weekday in theweek:
            week.append(self.formatday(d, events, events2, comments))
        return week
         
    def formatweekheader(self):
        s = [self.formatweekday(i) for i in self.iterweekdays()]
        return s

    def previous_month(self):
        month_num = self.month
        new_month = month_num
        new_year = self.year
        if new_year > 2021:
            if new_month == 1:
                new_month = 13
                new_year-= 1
        if 1 < new_month <= 12:
            new_month -=1
        else:
            new_month = 12

        return new_month, new_year

    def next_month(self):
        month_num = self.month
        new_month = month_num
        new_year = self.year
        if month_num <= 11:
            new_month +=1
        else:
            new_month -= new_month
            new_month +=1
            new_year += 1
        return new_month, new_year

    def formatmonth(self, withyear = True):
        events = Appointment.display(appointment_date__year=self.year, appointment_date__month=self.month)
        events2 = AppointmentResponse.display(appointment_date__year=self.year, appointment_date__month=self.month)
        comments = Comment.objects.filter(date__year=self.year, date__month=self.month, is_deleted=False)
        new_cal = {}
        cal = []
        new_cal.update({'headers':self.formatweekheader()})
        new_cal.update({'month_name':self.formatmonthname(self.year, self.month, withyear=withyear)['name']})
        for week in self.monthdays2calendar(self.year, self.month):
            cal.append(self.formatweek(week, events, events2, comments))
        new_cal.update({'month':cal})
        new_cal.update({'year_num':self.year})
        new_cal.update({'month_num':self.month})

        new_cal.update({'pre_month' : {'pre_month_num':self.previous_month()[0],'year_num':self.previous_month()[1] }})
        new_cal.update({'next_month' : {'next_month_num':self.next_month()[0],'year_num':self.next_month()[1] }})
        return new_cal

