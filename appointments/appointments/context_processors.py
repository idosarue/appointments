from therapist.models import Day
from therapist.forms import ContactFormEmailPatient, EditAppointmentForm, EditAppointmentResponseForm
from django.utils.translation import gettext_lazy as _

def day_processor(request):
    days = Day.disabled_days()          
    return {'days': days}


def form_proccesor(request):
    contact_form = ContactFormEmailPatient()
    edit_appoint_form = EditAppointmentForm()
    edit_response_form = EditAppointmentResponseForm()
    return {'contact_form': contact_form, 'edit_appoint_form':edit_appoint_form,'edit_response_form':edit_response_form}

def tabel_headers_proccesor(request):
    start_time = _('start time')
    appointment_date = _('appointment date')
    week_day = _('week day')
    first_name = _('first name')
    last_name = _('last name')
    patient_phone = _('patient phone')
    patient_email = _('patient email')
    requested_on = _('requested on')
    options = _('options')

    return {'start_time': start_time, 
    'appointment_date':appointment_date,
    'week_day':week_day,
    'first_name':first_name, 
    'last_name': last_name, 
    'patient_phone':patient_phone, 
    'patient_email': patient_email,
    'requested_on':requested_on,
    'options':options}

