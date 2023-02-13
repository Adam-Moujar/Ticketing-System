from django.test import TestCase, Client
from django.urls import reverse
from ticketing.models.users import User


class SpecialistInboxViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('specialist_dashboard')
        self.specialist = User.objects.create_specialist(
            email='johndoe@example.com',
            first_name='John',
            last_name='Doe',
            password='Password@123',
        )

        self.student = User.objects.create_user(
            email='janedoe@example.com',
            first_name='Jane',
            last_name='Doe',
            password='Password@123',
        )

        self.director = User.objects.create_director(
            email='bobdoe@example.com',
            first_name='Bob',
            last_name='Doe',
            password='Password@123',
        )

    def test_specialist_dashboard_url(self):
        self.assertEqual(self.url, '/specialist_dashboard/')

    def test_get_specialist_dashboard_as_student(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.student.email, password='Password@123'
        )

        self.assertTrue(loggedin)
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(
            response, response_url, status_code=302, target_status_code=200
        )

    def test_get_specialist_dashboard_as_director(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.director.email, password='Password@123'
        )

        self.assertTrue(loggedin)
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(
            response, response_url, status_code=302, target_status_code=200
        )
