from datetime import date, timedelta
from django.db import models
from datetime import datetime, time, timedelta
# Create your models here.

class Day(models.Model):
    name = models.CharField(max_length=200)
    week_day = models.IntegerField(default=0) 
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def disabled_days(cls):
        disabled_days_li = [disabled_day.week_day for disabled_day in cls.objects.filter(is_disabled=True)]
        return disabled_days_li
        
class Date(models.Model):
    date = models.DateField(null=True)
    is_disabled = models.BooleanField(default=False)

    @classmethod
    def disabled_dates(cls):
        disabled_dates_li = [disabled_date.date for disabled_date in cls.objects.filter(is_disabled=True)]
        return disabled_dates_li
# class NewDisabledDays(models.Model):
#     day = models.ForeignKey(Day, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.day.name

class WorkingTime(models.Model):
    # start_time = models.IntegerField(default=9)
    # minutes = models.IntegerField(default=30)
    # end_time = models.IntegerField(default=16)
    start_time = models.TimeField()
    # minutes = models.IntegerField(default=30)
    end_time = models.TimeField()
    break_time = models.IntegerField(default=15)


    @classmethod 
    def create_time_choice(cls):
        c = 0
        li = []
        start_time = cls.objects.first().start_time
        end_time = cls.objects.first().end_time
        break_time = WorkingTime.objects.first().break_time

        for x in range(start_time.hour , end_time.hour +1):
            y = datetime.combine(date.today(),time(hour=x, minute=start_time.minute))+timedelta(minutes=c)
            b = y + timedelta(hours=1)
            if b.time() < end_time:
                li.append((y.time(), f'{y.time().hour:02d}:{y.time().minute}'))
                c+=break_time

        # print(li)
        return li
