from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

def send_message_to_user(user, start_time, appointment_date):
    email_message_user = f'''
    Hello {user.username}, your request for an appointment for: {start_time} , {appointment_date}
    is being reviewed, we will get back to you soon.
    '''
    send_mail(
    'Appointment Request',
    email_message_user,
    'testdjangosaru@gmail.com',
    [user.email],
    )

def send_message_to_therapist(user, start_time, appointment_date, therapist_email):
    email_message_therapist = f'''
    {user.first_name} {user.last_name}, requested an appointment for: {start_time} , {appointment_date}
    '''
    send_mail(
    'Appointment Request',
    email_message_therapist,
    therapist_email,
    [therapist_email],
    )

def send_message_to_therapist_after_update(original_appointment,user, appointment, therapist_email):
    email_message_therapist = f'''
    {user.first_name} {user.last_name}, rejected your appointment update for: {original_appointment.start_time}, {original_appointment.appointment_date}
    and requested an appointment at: {appointment.start_time} , {appointment.appointment_date}
    '''
    send_mail(
    'Appointment Request',
    email_message_therapist,
    therapist_email,
    [therapist_email],
    )
    
def send_response_email_to_user(user, appointment, therapist_email):
        send_mail(
        'Appointment Request',
        'tests',
        therapist_email,
        [user.email],
        fail_silently=False,
        html_message= render_to_string(
            'therapist/email.html', 
            {'appointment': appointment,
                'user': user, 'domain' : Site.objects.get_current().domain,
                'protocol' : 'http',
            })
        )

def send_success_message_email_to_user(user, start_time, appointment_date, therapist_email):
        email_message_user = f'''
        Hello {user.first_name} {user.last_name}, your request for an appointment for: {start_time} ,{appointment_date}
        was approved.
        '''
        send_mail(
            'Appointment Request',
            email_message_user,
            therapist_email,
            [user.email],
        )


def send_success_message_email_to_therapist(user, start_time, appointment_date, therapist_email):
        email_message_therapist = f'''
        you approved an appointment for: {user.first_name} {user.last_name}, for: {start_time} ,{appointment_date}
        '''
        send_mail(
            'Appointment Request',
            email_message_therapist,
            therapist_email,
            [therapist_email],
        )

def send_success_repsponse_message_email_to_therapist(user, start_time, appointment_date, therapist_email):
        email_message_therapist = f'''
        {user.first_name} {user.last_name} approved an your updated request for an appointment, for: {start_time} ,{appointment_date}
        '''
        send_mail(
            'Appointment Request',
            email_message_therapist,
            therapist_email,
            [therapist_email],
        )