from therapist.models import Day

def day_processor(request):
    days = Day.disabled_days()          
    return {'day': days}