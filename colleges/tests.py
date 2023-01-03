from django.test import TestCase
from msilib.schema import RemoveRegistry
from urllib import response
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from colleges.views import CollegeDashboardView


class CollegeDashboardPageTests(TestCase):
    def setUp(self) -> None:
         self.response = self.client.get('/colleges/dashboard')

    def test_collegedashboard_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'colleges/college_dashboard.html')
    
    def test_collegedashboard_view(self):
        view = resolve('/colleges/dashboard')
        self.assertEqual(
            view.func.__name__,
            CollegeDashboardView.as_view().__name__
        )
# class HomepageTests(SimpleTestCase):
#     def setUp(self) -> None:
#         self.response = self.client.get(reverse('home'))

#     def test_homepage_template(self):
#         self.assertEqual(self.response.status_code, 200)
#         self.assertTemplateUsed(self.response, 'home.html')

#     def test_homepage_view(self):
#         view = resolve('/accounts/home/')
#         self.assertEqual(
#             view.func.__name__,
#             HomePageView.as_view().__name__
#         )

