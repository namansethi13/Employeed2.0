from msilib.schema import RemoveRegistry
from urllib import response
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from accounts.forms import CollegeSignUpForm, CorporateSignUpForm
from accounts.views import SignUpView, HomePageView
from accounts.custom_views import(
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView
) 

class HomepageTests(SimpleTestCase):
    def setUp(self) -> None:
        self.response = self.client.get(reverse('home'))

    def test_homepage_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_view(self):
        view = resolve('/accounts/home/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )


class SignupPageTests(TestCase):
    def setUp(self) -> None:
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Hi there')

    def test_signup_form_corporate(self):
        form = self.response.context.get('signup_corporate_form')
        self.assertIsInstance(form, CorporateSignUpForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_form_college(self):
        form = self.response.context.get('signup_college_form')
        self.assertIsInstance(form, CollegeSignUpForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(
            view.func.__name__,
            SignUpView.as_view().__name__
        )
        

class LoginPageTests(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get(reverse('login'))
    
    def test_login_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/login.html')
        self.assertNotContains(self.response, 'Hi there')
    
    def test_login_form(self):
        self.assertContains(self.response, 'form')
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_login_view(self):
        view = resolve('/accounts/login/')
        self.assertEqual(
            view.func.__name__,
            CustomLoginView.as_view().__name__
        )

class LogoutPageTests(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get(reverse('logout'))
    
    def test_logout_template(self):
        self.assertEqual(self.response.status_code, 302)
    
    def test_logout_view(self):
        view = resolve('/accounts/logout/')
        self.assertEqual(
            view.func.__name__,
            CustomLogoutView.as_view().__name__
        )

class PasswordChangePageTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('password_change'))

    def test_password_change_template(self):
        self.assertEqual(self.response.status_code, 302)
        self.assertTemplateNotUsed(self.response, 'accounts/password_change.html')
    
    def test_password_change_view(self):
        view = resolve('/accounts/password_change/')
        self.assertEqual(
            view.func.__name__,
            CustomPasswordChangeView.as_view().__name__
        )

