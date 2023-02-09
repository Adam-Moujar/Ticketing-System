from django.test import TestCase
from django import forms
from ticketing.forms import StudentTicketForm
from django.urls import reverse
from ticketing.models import User, Department


class CreateTicketViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('create_ticket')
        User.objects.create_user(
            email='johndoe@example.com',
            first_name='John',
            last_name='Doe',
            password='Password@123',
        )
        self.department = Department.objects.create(name='Accommodation')
        self.client.login(email='johndoe@example.com', password='Password@123')

    def test_create_ticket_url(self):
        self.assertEqual(self.url, '/create_ticket/')

    def test_get_create_ticket(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_ticket_form.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, StudentTicketForm))
        self.assertFalse(form.is_bound)

    def test_create_valid_ticket(self):
        user_pk = User.objects.get(pk=1).pk
        form_input = {
            'student': user_pk,
            'department': self.department.pk,
            'header': 'Lorem Ipsum',
            'content': 'Hello World',
        }
        response = self.client.post(self.url, form_input, follow=True)
        response_url = reverse('student_dashboard')
        self.assertRedirects(response, response_url)

    def test_ticket_with_no_department(self):
        user_pk = User.objects.get(pk=1).pk
        form_input = {
            'student': user_pk,
            'header': 'Lorem Ipsum',
            'content': 'Hello World',
        }
        response = self.client.post(self.url, form_input, follow=True)
        response_url = reverse('create_ticket')
        self.assertTemplateUsed(response, 'student_ticket_form.html')
        form = response.context['form']
        self.assertEqual(list(form.errors.keys()), ['department'])
        self.assertTrue(isinstance(form, StudentTicketForm))

    def test_ticket_with_no_header(self):
        user_pk = User.objects.get(pk=1).pk
        form_input = {
            'student': user_pk,
            'department': self.department.pk,
            'content': 'Hello World',
        }
        response = self.client.post(self.url, form_input, follow=True)
        response_url = reverse('create_ticket')
        self.assertTemplateUsed(response, 'student_ticket_form.html')
        form = response.context['form']
        self.assertEqual(list(form.errors.keys()), ['header'])
        self.assertTrue(isinstance(form, StudentTicketForm))

    def test_ticket_with_no_content(self):
        user_pk = User.objects.get(pk=1).pk
        form_input = {
            'student': user_pk,
            'department': self.department.pk,
            'header': 'Lorem Ipsum',
        }
        response = self.client.post(self.url, form_input, follow=True)
        response_url = reverse('create_ticket')
        self.assertTemplateUsed(response, 'student_ticket_form.html')
        form = response.context['form']
        self.assertEqual(list(form.errors.keys()), ['content'])
        self.assertTrue(isinstance(form, StudentTicketForm))
