from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from datetime import datetime, timedelta, date
from patient.models import Appointment

therapist_email = 'testdjangosaru@gmail.com'

def send_message_to_user(user, start_time, appointment_date):
    email_message_user = f'''
    Hello {user.username}, your request for an appointment for: {start_time} , {appointment_date}
    is being reviewed, we will get back to you soon.
    '''
    send_mail(
    'Appointment Request',
    email_message_user,
    therapist_email,
    [user.email],
    )

def send_message_to_therapist(user, start_time, appointment_date):
    email_message_therapist = f'''
    {user.first_name} {user.last_name}, requested an appointment for: {start_time} , {appointment_date}
    '''
    send_mail(
    'Appointment Request',
    email_message_therapist,
    therapist_email,
    [therapist_email],
    html_message= render_to_string(
    'therapist/emails/email_to_therapist.html', 
    {'user': user, 'domain' : Site.objects.get_current().domain,
    'protocol' : 'http',
    'start_time' : start_time,
    'appointment_date' : appointment_date,
    })
    )

def send_message_to_therapist_after_update(original_appointment,user, appointment):
    email_message_therapist = f'''
    {user.first_name} {user.last_name}, rejected your appointment update for: {original_appointment.start_time}, {original_appointment.appointment_date}
    and requested an appointment at: {appointment.start_time} , {appointment.appointment_date}
    '''
    send_mail(
    'Appointment Update',
    email_message_therapist,
    therapist_email,
    [therapist_email],
    html_message= render_to_string(
    'therapist/emails/email_therapist_after_update.html', 
    {'user': user, 'domain' : Site.objects.get_current().domain,
    'protocol' : 'http',
    'appointment' : appointment,
    'original_appointment' : original_appointment
    })
    )
  
def send_response_email_to_user(user, appointment):
        send_mail(
        'Appointment Update',
        'tests',
        therapist_email,
        [user.email],
        fail_silently=False,
        html_message= render_to_string(
            'therapist/emails/email.html', 
            {'appointment': appointment,
                'user': user, 'domain' : Site.objects.get_current().domain,
                'protocol' : 'http',
            })
        )

def send_success_message_email_to_user(user, start_time, appointment_date):
        email_message_user = f'''
        Hello {user.first_name} {user.last_name}, your request for an appointment for: {start_time} ,{appointment_date}
        was approved.
        '''
        send_mail(
            'Appointment Approved',
            email_message_user,
            therapist_email,
            [user.email],
        )


def send_success_message_email_to_therapist(user, start_time, appointment_date):
        email_message_therapist = f'''
        you approved an appointment for: {user.first_name} {user.last_name}, for: {start_time} ,{appointment_date}
        '''
        send_mail(
            'Appointment Approved',
            email_message_therapist,
            therapist_email,
            [therapist_email],
        )

def send_success_repsponse_message_email_to_therapist(user, start_time, appointment_date):
        email_message_therapist = f'''
        {user.first_name} {user.last_name} approved an your updated request for an appointment, for: {start_time} ,{appointment_date}
        '''
        send_mail(
            'Appointment Approved',
            email_message_therapist,
            therapist_email,
            [therapist_email],
        )
def send_contact_message_to_patient(user_email, subject, body):
        send_mail(
            subject,
            body,
            therapist_email,
            [user_email],
        )

def send_contact_message_to_therapist(user_email, subject, body):
        subject_send = f'{user_email} sent you a contact message:{subject}'
        email = EmailMessage(
        subject_send,
        body,
        therapist_email,
        [therapist_email],
        reply_to=[user_email],
        )

        email.send()

# def send_reminder_email(today):
#         x = today + timedelta(days=1)
#         a = Appointment.display()
#         print(x)
#         for i in a:
#             if i.appointment_date == x.date():
#                 email_message_therapist = f'''
#                 Hello {i.user.user.first_name} {i.user.user.last_name} reminder, for: an appointment tommorow at {i.start_time},
#                 '''
#                 send_mail(
#                 'Appointment Reminder',
#                 email_message_therapist,
#                 therapist_email,
#                 [i.user.user.email],
#                 )