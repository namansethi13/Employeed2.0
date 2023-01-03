from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.encoding import force_str 
from django.urls import reverse_lazy
from django.contrib import messages
from colleges.models import CollegeModel
from corporates.models import CorporateModel
from .choices import RoleType, ShortRoleType
from .forms import SignUpForm
from .utils import check_email, send_activation_email, format_email_message  
from .tokens import account_activation_token
import logging
import random

from .custom_decorators import logout_required

logger = logging.getLogger(__name__)

class HomePageView(TemplateView):
    """
    Home Page of Website
    """
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'home.html')
        elif request.user.role == ShortRoleType.COLLEGE:
            return redirect('college_dashboard')
        elif request.user.role == ShortRoleType.CORPORATE:
            return redirect('job_list')
        elif request.user.role == RoleType.STUDENT:
            return redirect('student_dashboard')

class SignUpView(CreateView):
    """
    SignUp View for Corporate and College
    """
    @method_decorator(logout_required)
    def get(self, request):
        """
        renders corporate and college form
        """
        context = {
            'signup_form' : SignUpForm()
        }
        return render(request, 'accounts/signup.html', context)

    @method_decorator(logout_required)
    def post(self, request):
        """
        Check the role and accordingly validate the post data
        """
        try:
            role = request.POST['role']
            pass1 =  request.POST['password1']
            pass2 =  request.POST['password2']
            if pass1 != pass2:
                messages.warning(request,"password do not match")
                logger.info("password do not match")
                return redirect(reverse_lazy('signup'))

            if role == ShortRoleType.CORPORATE or role == ShortRoleType.COLLEGE:
                form = SignUpForm(request.POST)
                # check email entered is already is in database
                redirect_url = check_email(request, request.POST.get('email',None))
                if redirect_url != None:
                    return redirect(redirect_url)
                if form.is_valid():
                    print("Form is valid")
                    email = form.cleaned_data.get('email')
                    username = email.split('@')[0] + str(random.randint(0,99999))
                    password= form.cleaned_data.get('password1')
                    
                    if role == ShortRoleType.CORPORATE:
                        user = CorporateModel.objects.create(username=username, email=email, 
                        password=password, role=ShortRoleType.CORPORATE)
                    else:
                        user = CollegeModel.objects.create(username=username, email=email, 
                        password=password, role=ShortRoleType.COLLEGE)
                    
                    user.set_password(password)
                    user.save()
                    logger.info("Registration Successfull!!")

                    message = format_email_message(request, user)
                    send_activation_email.delay(message, email)
                    logger.info(f"email sent to {email}")
                    messages.success(request,f"check {email} to get a verification link")
                else:
                    messages.warning(request,"Form data is invalid")
            else:
                logger.warning("Role should be Collge or Corporate")
                messages.warning(request, "Error: role should be of College or Corporate")
            return redirect(reverse_lazy('signup'))
        except:
            logger.error("Error: Some exception occurred at post request")
            messages.error(request, "Error: Some exception occurred at post request")
            return redirect(reverse_lazy('home'))

def activate(request, uidb64, token):
    """
    activate the user isntance after verifying the email
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        logger.debug("Email verified successfully !!")
        messages.success(request, "Email verified successfully !!")
        return redirect(reverse_lazy('login'))
    else:
        logger.warning("Email Activation link is corrupted !!")
        messages.warning(request, "Email Activation link is corrupted !!")
        return redirect(reverse_lazy('home'))
