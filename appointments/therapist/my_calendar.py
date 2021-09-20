from datetime import date, datetime, timedelta
from calendar import HTMLCalendar
from patient.models import Appointment, AppointmentResponse
from therapist.models import Date, Day, Comment
from django.urls import reverse_lazy
import holidays
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
    
    def formatday(self, day, events, events2, comments):
        events_per_day = events.filter(appointment_date__day=day).order_by('start_time')
        events_per_day2 = events2.filter(appointment_date__day=day).order_by('start_time')
        comments = comments.filter(date__day=day)
        d = ''
        a = '''
        <div id="exampleModal" class="modal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title">Modal title</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
                </div>
                <div class="modal-body">
                <form action="{% url 'working_time' %}" method="POST">
                    {% csrf_token %}
                    {{working_form.as_p}}
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Save changes</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </form>
                </div>

            </div>
            </div>
        </div>
        <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
            Edit Working time
        </button>
        '''
        # for comment in comments:
        #     a += f'<li class="comment"><a href="{reverse_lazy("edit_comment", kwargs={"pk":comment.id})}">{comment.content}</a> <a class="comment-confirm-delete" href="{reverse_lazy("delete_comment", kwargs={"pk":comment.id})}">delete comment</a></li>'

        for event in events_per_day:
            print()
            d += f'<li> {event.start_time} {event.user.user.first_name} {event.user.user.last_name} {event.user.phone_number} <a  href="{reverse_lazy("update_apt", kwargs={"pk":event.id})}">edit</a> <br> <a href="{reverse_lazy("delete_appointment", kwargs= {"pk" :event.id})}" class="confirm_delete">Cancel</a></li>'

        for event in events_per_day2:
            d += f'<li> {event.start_time} {event.user.user.first_name} {event.user.user.last_name} {event.user.phone_number} <a href="{reverse_lazy("update_apt_res", kwargs={"pk":event.id})}">edit</a> <br><a href="{reverse_lazy("delete_appointment_response", kwargs= {"pk" :event.id})}" class="confirm_delete">Cancel</a></li>'

        if day:
            v_date = date(self.year, self.month, day)
            isr_holidays = holidays.CountryHoliday('ISR')
            holi = ''
            link = f"<a href='{reverse_lazy('create_comment', kwargs={'year': self.year, 'month': self.month, 'day': day})}'>add comment</a>"
            if v_date in isr_holidays:
                holi += isr_holidays.get(f'{v_date.year}-{v_date.month}-{v_date.day}')
                # print(holi)
            if v_date > date.today() and not v_date.weekday() in Day.disabled_days() and not v_date in Date.disabled_dates():
                return f"<td id='{day}'><span class='date'>{day} {link} {holi} <a href='{reverse_lazy('create_appoint', kwargs={'year': self.year, 'month': self.month, 'day': day})}'>+</a> </span><ul>{d}</ul>{a}</td>"
            elif v_date.weekday() in Day.disabled_days() or v_date in Date.disabled_dates():
                return f"<td id='{day}'><span class='date'>{day} {link}  {holi}</span><ul>{d}</ul> <span class='dis'>disabled</span>{a}</td>"
            else:
                return f"<td id='{day}'><span class='date'>{day} {link} {holi}</span><ul>{d}</ul>{a}</td>"
        
        return '<td></td>'

    def formatweek(self, theweek, events, events2, comments):
        week = ''
   
        for d, weekday in theweek:
            print(d)
            week += self.formatday(d, events, events2, comments)
            
        return f'<tr> {week} </tr>'
    
    def formatmonth(self, withyear = True):
        events = Appointment.display(appointment_date__year=self.year, appointment_date__month=self.month)
        events2 = AppointmentResponse.display(appointment_date__year=self.year, appointment_date__month=self.month)
        comments = Comment.objects.filter(date__year=self.year, date__month=self.month, is_deleted=False)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar table table-primary">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, events2, comments)}'
            print(week)
        return cal