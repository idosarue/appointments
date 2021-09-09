from datetime import datetime, timedelta
from calendar import HTMLCalendar
from patient.models import Appointment, AppointmentResponse

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
    
    def formatday(self, day, events, events2):
        events_per_day = events.filter(appointment_date__day=day)
        events_per_day2 = events2.filter(appointment_date__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li> {event.user.user.first_name} {event.user.user.last_name} {event.start_time}</li>'

        for event in events_per_day2:
            d += f'<li> {event.user.user.first_name} {event.user.user.last_name} {event.start_time}</li>'

        if day:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events, events2):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, events2)
        return f'<tr> {week} </tr>'
    
    def formatmonth(self, withyear = True):
        events = Appointment.objects.filter(appointment_date__year=self.year, appointment_date__month=self.month, is_approved=True)
        events2 = AppointmentResponse.objects.filter(appointment_date__year=self.year, appointment_date__month=self.month, is_approved=True)
       	cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, events2)}'
        return cal