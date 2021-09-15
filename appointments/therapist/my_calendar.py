from datetime import date, datetime, timedelta
from calendar import HTMLCalendar
from patient.models import Appointment, AppointmentResponse
from therapist.models import Date, Day
from django.urls import reverse_lazy
import holidays
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
    
    def formatday(self, day, events, events2):
        events_per_day = events.filter(appointment_date__day=day).order_by('start_time')
        events_per_day2 = events2.filter(appointment_date__day=day).order_by('start_time')
        d = ''
        for event in events_per_day:
            print()
            d += f'<li> {event.start_time} {event.user.user.first_name} {event.user.user.last_name} {event.user.phone_number} <a  href="{reverse_lazy("update_apt", kwargs={"pk":event.id})}">edit</a> <br> <a href="{reverse_lazy("delete_appointment", kwargs= {"pk" :event.id})}" class="confirm_delete">Cancel</a></li>'

        for event in events_per_day2:
            d += f'<li> {event.start_time} {event.user.user.first_name} {event.user.user.last_name} {event.user.phone_number} <a href="{reverse_lazy("update_apt_res", kwargs={"pk":event.id})}">edit</a> <br><a href="{reverse_lazy("delete_appointment_response", kwargs= {"pk" :event.id})}" class="confirm_delete">Cancel</a></li>'

        if day:
            v_date = date(self.year, self.month, day)
            isr_holidays = holidays.CountryHoliday('ISR')
            holi = ''
            if v_date in isr_holidays:
                holi += isr_holidays.get(f'{v_date.year}-{v_date.month}-{v_date.day}')
                # print(holi)
            if v_date > date.today() and not v_date.weekday() in Day.disabled_days() and not v_date in Date.disabled_dates():
                return f"<td><span class='date'>{day} {holi}  <a href='{reverse_lazy('create_appoint', kwargs={'year': self.year, 'month': self.month, 'day': day})}'>+</a> </span><ul>{d}</ul></td>"
            else:
                return f"<td><span class='date'>{day}  {holi}</span><ul>{d}</ul> <span class='dis'>disabled</span></td>"
        
        return '<td></td>'

    def formatweek(self, theweek, events, events2):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, events2)
        return f'<tr> {week} </tr>'
    
    def formatmonth(self, withyear = True):
        events = Appointment.display(appointment_date__year=self.year, appointment_date__month=self.month)
        events2 = AppointmentResponse.display(appointment_date__year=self.year, appointment_date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, events2)}'
        return cal