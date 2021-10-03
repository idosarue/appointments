from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from datetime import datetime, timedelta, date
from patient.models import Appointment
import os
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# Build paths inside the project like this: BASE_DIR / 'subdir'.




therapist_email = 'testdjangosaru@gmail.com'
therapist_email_reciever = 'djangoreciever@gmail.com'

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

def send_message_to_user(user, start_time, appointment_date):
    email_message_user = f'''
    Hello {user.username}, your request for an appointment for: {start_time} , {appointment_date}
    is being reviewed, we will get back to you soon.
    '''
    message = Mail(
    from_email=therapist_email,
    to_emails=user.email,
    subject='Appointment Request',
    html_content=email_message_user)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

def send_message_to_therapist(user, start_time, appointment_date):
    message = Mail(
    from_email=therapist_email,
    to_emails=therapist_email_reciever,
    subject='Appointment Request',
    html_content=render_to_string(
    'therapist/emails/email_to_therapist.html', 
    {'user': user, 'domain' : Site.objects.get_current().domain,
    'protocol' : 'http',
    'start_time' : start_time,
    'appointment_date' : appointment_date,
    }))

    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

def send_message_to_therapist_after_update(original_appointment,user, appointment):
    message = Mail(
    from_email=therapist_email,
    to_emails=therapist_email_reciever,
    subject='Appointment Request',
    html_content=render_to_string(
    'therapist/emails/email_therapist_after_update.html', 
    {'user': user, 'domain' : Site.objects.get_current().domain,
    'protocol' : 'http',
    'appointment' : appointment,
    'original_appointment' : original_appointment
    }))

    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

    
def send_response_email_to_user(user, appointment):
        message = Mail(
        from_email=therapist_email,
        to_emails=user.email,
        subject='Appointment Request',
        html_content=render_to_string(
        'therapist/emails/email.html', 
        {'appointment': appointment,
            'user': user, 'domain' : Site.objects.get_current().domain,
            'protocol' : 'http',
        }))

        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)


def send_success_message_email_to_user(user, start_time, appointment_date):
        email_message_user = f'''
        Hello {user.first_name} {user.last_name}, your request for an appointment for: {start_time} ,{appointment_date}
        was approved.
        '''

        message = Mail(
        from_email=therapist_email,
        to_emails=user.email,
        subject='Appointment Approved',
        html_content=email_message_user)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)


def send_success_message_email_to_therapist(user, start_time, appointment_date):
        email_message_therapist = f'you approved an appointment for: {user.first_name} {user.last_name}, for: {start_time} ,{appointment_date}'        
        message = Mail(
        from_email=therapist_email,
        to_emails=therapist_email_reciever,
        subject='Appointment Approved',
        html_content=email_message_therapist)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)


def send_success_repsponse_message_email_to_therapist(user, start_time, appointment_date):
        email_message_therapist = f'''
        {user.first_name} {user.last_name} approved an your updated request for an appointment, for: {start_time} ,{appointment_date}
        '''

        message = Mail(
        from_email=therapist_email,
        to_emails=therapist_email_reciever,
        subject='Appointment Approved',
        html_content=email_message_therapist)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)




def send_contact_message_to_patient(user_email, subject, body):
    message = Mail(
    from_email=therapist_email,
    to_emails=user_email,
    subject=subject,
    html_content=body)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)



def send_contact_message_to_therapist(user_email, subject, body):
        subject_send = f'{user_email} sent you a contact message:{subject}'
        email = EmailMessage(
        subject_send,
        body,
        therapist_email,
        [therapist_email_reciever],
        reply_to=[user_email],
        )
        print(subject_send)
        email.send()
