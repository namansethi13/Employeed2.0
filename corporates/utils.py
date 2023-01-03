from django.core import mail
from django.template.loader import render_to_string 
from core.settings import DEFAULT_FROM_EMAIL
import logging

logger = logging.getLogger(__name__)

def send_test_details(students, domain, job_id):
    """
    Detial of Job and Test for first round to all the eligible courses
    """
    try:
        connection = mail.get_connection()
        connection.open()
        logger.info("Mail connection Opened")

        mail_subject = 'New Jobs for you'
        email_msg = []
        for student in students:
            if student.is_active:
                message = render_to_string('corporates/email_job_post.html', {
                    'username' : student.username,
                    'domain' : domain,
                    'job_id' : job_id,
                })
                email_msg.append(
                    mail.EmailMessage(
                        subject=mail_subject,
                        body=message,
                        from_email=DEFAULT_FROM_EMAIL,
                        to=[student.email]
                    )
                )
        connection.send_messages(email_msg)
        logger.info("Job and Test Details Email sent Successfully")
    except:
        logger.error("couldn't sent the Job and Test Details Mail to the Eligible Course Students")
    finally:
        connection.close()