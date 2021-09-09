import datetime
from django import forms
from django.db import models
from datetime import time

from django.db.models.enums import Choices
from .utils import Calendar

YEAR_CHOICES = [(x+2021,y) for x,y in enumerate(list(range(2021,2051)))]
month_li = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
MONTH_CHOICES = [(x,y) for x,y in enumerate(month_li, 1)]
class CalendarForm(forms.Form):
    year = forms.ChoiceField(choices = YEAR_CHOICES)
    month = forms.ChoiceField(choices = MONTH_CHOICES)
