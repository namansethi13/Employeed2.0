from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse_lazy 
from .tokens import account_activation_token
from celery import shared_task

import logging

logger = logging.getLogger(__name__)

def check_email(request, to_email):
    """
    Checks every signup request, wheater email entered is already exists in database.
    if exists and not activated, then send a activated email
    elif exists and activated, redirected to the login page
    else contine to signup the new user and send a activation email
        by calling send_activation_email(request, user, form=None, to_email=to_email)
    """
    try:
        if get_user_model().objects.filter(email__exact = to_email).exists():
            user = get_user_model().objects.get(email__exact = to_email)
            if (user.is_active and user.is_email_verified):
                logger.debug("User with this email has activated account, pls login")
                messages.info(request, "User with this email has activated account, pls login")
                return reverse_lazy('login')
            else:
                message = format_email_message(request, user)
                send_activation_email.delay(message, to_email=to_email)
                logger.warning("User with this email already exists. Check your inbox for email verification link")
                messages.info(request, "User with this email already exists. Check your inbox for email verification link")
                return reverse_lazy('login')
    except:
        logger.error("email data is invalid !!")
        messages.error(request, "email data is invalid !!")
        return reverse_lazy('signup')

    return None

def format_email_message(request, user):
    current_site = get_current_site(request)
    message = render_to_string('accounts/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
    })
    return message

@shared_task
def send_activation_email(message, to_email=None):
    """
    Send activation email to the user, entered in the form data.
    template is in accounts app at 'templates/accounts/acc_active_email.html'. 
    """
    try:
        mail_subject = 'Activate your account.'
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
    except:
        logger.error("couldn't sent the activation email, pls try to signup after some time..")
        raise Exception("Error: couldn't sent the activation email, pls try to signup after some time..")