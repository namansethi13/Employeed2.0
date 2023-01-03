from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string 
from django.core import mail
from django.contrib import messages 
from accounts.tokens import account_activation_token
from core.settings import DEFAULT_FROM_EMAIL
from .exceptions import StudentEmailSendException, CollegeEmailSendException
import logging

logger = logging.getLogger(__name__)

def notify_through_email(college_obj, course_obj):
    """
    Send notifying email to the college to notify about account creatign of student for a particular course
    template is in colleges app at 'templates/colleges/college_notify.html'. 
    """
    try:
        mail_subject = 'Activate your account.'
        message = render_to_string('colleges/college_notify.html', {
            'user': college_obj.username,
            'course' : course_obj.full_name
        })
        email = mail.EmailMessage(
                    mail_subject, message, to=[college_obj.email]
        )
        email.send()
        logger.info("Notified the college throught email")
    except:
        logger.error("Failed to email college")
        raise CollegeEmailSendException()


def send_credentials_email(domain, users, passwords):
    """
    Send activation email to the students from the users list param
    template is in colleges app at 'templates/colleges/student_credential_email.html'. 
    """
    try:
        # gettign the connection for sending emails
        connection = mail.get_connection()
        connection.open()
        logger.info("Mail connection Opened")

        mail_subject = 'Activate your account'

        # making differnt email's body for different users
        email_msg = []
        for i in range(0, len(users)):
            users[i].set_password(passwords[i])
            users[i].save()
            message = render_to_string('colleges/student_credential_email.html', {
                'user': users[i],
                'domain': domain,
                'uid':urlsafe_base64_encode(force_bytes(users[i].pk)),
                'token':account_activation_token.make_token(users[i]),
                'email' : users[i].email,
                'password' : passwords[i]
            })
            email_msg.append(
                mail.EmailMessage(
                    subject=mail_subject,
                    body=message,
                    from_email=DEFAULT_FROM_EMAIL,
                    to=[users[i].email]
                )
            )
        
        connection.send_messages(email_msg)
        logger.info("Email sent Successfully to all students")  
    except:
        logger.error("couldn't sent the activation email, pls try to upload after some time..")
        raise StudentEmailSendException()
    finally:
        connection.close()