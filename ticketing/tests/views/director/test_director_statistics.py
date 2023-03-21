from django.test import TestCase, Client
from django.urls import reverse
from ticketing.models import User, Department, Message
from ticketing.models.specialist import SpecialistInbox, SpecialistDepartment
from ticketing.models.tickets import SpecialistMessage, Ticket
from ticketing.tests.helpers import (
    FixtureHelpers,
    reverse_with_next,
    get_tickets,
)


class SpecialistStatisticsViewTestCase(TestCase):

    fixtures = [
        'ticketing/tests/fixtures/user_fixtures.json',
        'ticketing/tests/fixtures/message_fixtures.json',
        'ticketing/tests/fixtures/ticket_fixtures.json',
        'ticketing/tests/fixtures/department_fixtures.json',
        'ticketing/tests/fixtures/specialist_inbox_fixtures.json',
        'ticketing/tests/fixtures/specialist_department_fixtures.json',
        'ticketing/tests/fixtures/student_message_fixtures.json',
        'ticketing/tests/fixtures/specialist_message_fixtures.json'
    ]

    def setUp(self):
        self.url = reverse(
            'director_statistics'
        )

        self.specialist = User.objects.filter(role='SP').first()
        self.student = User.objects.filter(role='ST').first()
        self.director = User.objects.filter(role='DI').first()

    def test_director_statistics_url(self):
        self.assertEqual(self.url, '/director_statistics')

    def test_get_director_statistics_as_student(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.student.email, password='Password@123'
        )

        self.assertTrue(loggedin)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_director_statistics_as_director(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.director.email, password='Password@123'
        )

        self.assertTrue(loggedin)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'director_statistics.html')

    def test_get_director_statistics_as_specialist(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )

        self.assertTrue(loggedin)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 403)

    def test_get_director_statistics_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, 'login.html')


    def test_length_of_ticket_list_is_equal_to_zero(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.director.email, password='Password@123'
        )
        Ticket.objects.all().delete()
        Message.objects.all().delete()
        response = self.client.get(self.url)
        data = response.context["object_list"]
        tickets = data[1].get('data')[1].get('value')
        self.assertEqual(tickets,0)
