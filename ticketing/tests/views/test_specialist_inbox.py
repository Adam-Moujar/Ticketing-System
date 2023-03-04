from django.test import TestCase, Client
from django.urls import reverse
from ticketing.models.users import User
from ticketing.models.specialist import SpecialistInbox, SpecialistDepartment
from ticketing.models.tickets import Ticket
from ticketing.tests.helpers import (
    FixtureHelpers,
    reverse_with_next,
    get_tickets,
)


class SpecialistInboxViewTestCase(TestCase):

    fixtures = [
        'ticketing/tests/fixtures/user_fixtures.json',
        'ticketing/tests/fixtures/message_fixtures.json',
        'ticketing/tests/fixtures/ticket_fixtures.json',
        'ticketing/tests/fixtures/department_fixtures.json',
        'ticketing/tests/fixtures/specialist_inbox_fixtures.json',
        'ticketing/tests/fixtures/specialist_department_fixtures.json',
    ]

    def setUp(self):
        self.url = reverse(
            'specialist_dashboard', kwargs={'ticket_type': 'personal'}
        )

        self.specialist = User.objects.filter(role='SP').first()
        self.student = User.objects.filter(role='ST').first()
        self.director = User.objects.filter(role='DI').first()

    def test_specialist_dashboard_url(self):
        self.assertEqual(self.url, '/specialist_dashboard/personal/')

    def test_get_specialist_dashboard_as_student(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.student.email, password='Password@123'
        )

        self.assertTrue(loggedin)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_specialist_dashboard_as_director(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.director.email, password='Password@123'
        )

        self.assertTrue(loggedin)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_specialist_dashboard_as_specialist(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )

        self.assertTrue(loggedin)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'specialist_dashboard.html')

    def test_get_specialist_dashboard_when_logged_out(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(
            response, redirect_url, status_code=302, target_status_code=200
        )
        self.assertTemplateUsed(response, 'login.html')

    def test_initial_inbox_is_personal(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.context['ticket_type'], 'personal')

    def test_personal_inbox_shows_correct_tickets(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )

        view_table = []

        response = self.client.get(
            reverse('specialist_dashboard', kwargs={'ticket_type': 'personal'})
        )

        num_pages = response.context['page_obj'].paginator.num_pages

        for i in range(1, num_pages + 1):
            response = self.client.get(
                reverse(
                    'specialist_dashboard', kwargs={'ticket_type': 'personal'}
                ),
                {'page': i},
            )

            for ticket in response.context['object_list']:
                view_table.append(ticket)

        right_ticket_list = get_tickets(self.specialist, 'personal')

        for ticket in right_ticket_list:
            self.assertTrue(ticket in view_table)

    def test_department_inbox_shows_correct_tickets(self):
        SpecialistInbox.objects.all().delete()
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )

        view_table = []

        response = self.client.get(
            reverse(
                'specialist_dashboard', kwargs={'ticket_type': 'department'}
            )
        )

        num_pages = response.context['page_obj'].paginator.num_pages

        for i in range(1, num_pages + 1):
            response = self.client.get(
                reverse(
                    'specialist_dashboard',
                    kwargs={'ticket_type': 'department'},
                ),
                {'page': i},
            )

            for ticket in response.context['object_list']:
                view_table.append(ticket)

        right_ticket_list = get_tickets(self.specialist, 'department')

        for ticket in right_ticket_list:
            self.assertTrue(ticket in view_table)

    def test_archived_inbox_shows_correct_tickets(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )

        view_table = []

        response = self.client.get(
            reverse('specialist_dashboard', kwargs={'ticket_type': 'archived'})
        )

        num_pages = response.context['page_obj'].paginator.num_pages

        for i in range(1, num_pages + 1):
            response = self.client.get(
                reverse(
                    'specialist_dashboard', kwargs={'ticket_type': 'archived'}
                ),
                {'page': i},
            )

            for ticket in response.context['object_list']:
                view_table.append(ticket)

        right_ticket_list = get_tickets(self.specialist, 'archived')

        for ticket in right_ticket_list:
            self.assertTrue(ticket in view_table)

    def test_view_ticket_info_redirect(self):
        SpecialistInbox.objects.all().delete()
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )
        self.url = reverse(
            'specialist_dashboard', kwargs={'ticket_type': 'department'}
        )
        response = self.client.get(self.url)
        view_table = response.context['object_list']
        ticket_id = view_table[0].id
        url = f'specialist_claim_ticket/{ticket_id}'
        self.assertIn(str.encode(url), response.content)
