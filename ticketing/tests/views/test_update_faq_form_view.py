from django.test import TestCase, Client
from ticketing.models import User, FAQ, Department, SpecialistDepartment
from ticketing.models.departments import Subsection
from django.utils.text import slugify
from django.urls import reverse


class UpdateFAQFormView(TestCase):
    fixtures = [
        'ticketing/tests/fixtures/user_fixtures.json',
        'ticketing/tests/fixtures/message_fixtures.json',
        'ticketing/tests/fixtures/ticket_fixtures.json',
        'ticketing/tests/fixtures/department_fixtures.json',
        'ticketing/tests/fixtures/specialist_inbox_fixtures.json',
        'ticketing/tests/fixtures/specialist_department_fixtures.json',
    ]

    def setUp(self):
        self.specialist = User.objects.filter(role='SP').first()
        self.student = User.objects.filter(role='ST').first()
        self.director = User.objects.filter(role='DI').first()
        self.department = Department.objects.create(
            name='Technology Help', slug=slugify('Technology Help')
        )
        self.subsection = Subsection.objects.create(
            department=self.department, name='Help needed'
        )
        self.faq = FAQ.objects.create(
            department=self.department,
            specialist=self.specialist,
            questions='What is 9+10?',
            subsection=self.subsection,
            answer='19',
        )
        self.url = reverse('faq_update', kwargs={'pk': self.faq.pk})

    def test_unauthenticated_user_cannot_access_update_faq_view(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
            status_code=302,
            target_status_code=200,
        )

    def test_user_without_required_role_cannot_access_update_faq_view(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.student.email, password='Password@123'
        )

        self.assertTrue(loggedin)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_user_with_required_role_can_access_update_faq_view(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_submission_redirects_update_faq_view_to_home_page(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )
        self.assertTrue(loggedin)
        response = self.client.get(self.url, follow=True)

        subsection = Subsection.objects.create(
            name='Updated Pain', department=self.department
        )
        response = self.client.post(
            self.url,
            {
                'questions': 'Updated question?',
                'subsection': str(subsection.id),
                'answer': 'Updated answer',
            },
        )
        self.assertTemplateUsed(response, 'index.html')

    # def test_form_submission_updates_faq_object(self):
    # self.client = Client()
    # loggedin = self.client.login(
    #     email=self.specialist.email,
    #     password="Password@123"
    # )
    # self.assertTrue(loggedin)
    # response = self.client.get(self.url, follow=True)
    # subsection = Subsection.objects.create(name = 'Updated Pain', department = self.department)

    # self.client.post(
    #     self.url,
    #     {'questions': 'Updated question?','subsection':subsection, 'answer': 'Updated answer'},
    # )

    # self.assertTemplateUsed(response, 'faq_update.html')

    # updated_faq = FAQ.objects.get(pk=self.faq.pk)
    # self.assertEquals(updated_faq.questions, 'Updated question?')
    # self.assertEquals(updated_faq.subsection,subsection)
    # self.assertEquals(updated_faq.answer, 'Updated answer')
