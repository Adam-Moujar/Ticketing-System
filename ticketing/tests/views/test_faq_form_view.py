from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser
from django.utils.text import slugify
from django.urls import reverse
from ticketing.models.users import User
from ticketing.models.departments import Department, Subsection
from ticketing.models.specialist import SpecialistDepartment
from ticketing.models.faq import FAQ
from ticketing.views.specialist_faq_form import FAQFormView

class FAQFormViewTest(TestCase):
    def setUp(self):
        self.url = reverse('faq_form_view')
        self.factory = RequestFactory()
        self.specialist = User.objects.create_specialist(
            email='specialist_user@email.com',
            first_name='James',
            last_name='Bond',
            password='Password@123',
        )
        self.department = Department.objects.create(
            name='Health and Safety',
            slug=slugify('Health and Safety'),
        )
        self.subsection = Subsection.objects.create(
            name='Updated Pain', department=self.department
        )
        SpecialistDepartment.objects.create(
            specialist=self.specialist, department=self.department
        )
        
        self.faq = FAQ.objects.create(
            specialist=self.specialist,
            department=self.department,
            subsection=self.subsection,
            question='What is the meaning of existence',
            answer='This question cannot be computed... error',
        )
        self.form_data = {
            'question': 'What is Django?',
            'subsection': str(self.subsection.id),
            'answer': 'Django is a high-level Python web framework.',
        }

    def test_faq_form_url(self):
        self.assertEqual(self.url, reverse('faq_form_view'))

    def test_get_faq_form(self):
        request = self.factory.get(reverse('faq_form_view'))
        request.user = self.specialist
        response = FAQFormView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FAQ.objects.count(), 1)

    def test_post_valid_faq_form(self):
        self.client = Client()
        self.client.login(
            email=self.specialist.email, password='Password@123'
        )
        response = self.client.get(self.url)
        response = self.client.post(
            self.url,
            self.form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FAQ.objects.count(), 2)

    def test_post_invalid_faq_form(self):
        request = self.factory.post(reverse('faq_form_view'), data={})
        request.user = self.specialist
        response = FAQFormView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FAQ.objects.count(), 1)

    def test_log_in_required_to_access_faq_form(self):
        request = self.factory.get(reverse('faq_form_view'))
        request.user = AnonymousUser()
        response = FAQFormView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('login') + '?next=' + reverse('faq_form_view'),
        )

    def test_role_required_to_access_faq_form(self):
        request = self.factory.get(reverse('faq_form_view'))
        request.user = self.specialist
        response = FAQFormView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        request.user = AnonymousUser()
        response = FAQFormView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_faq_form_view_uses_correct_template(self):
        request = self.factory.get(reverse('faq_form_view'))
        request.user = self.specialist
        response = FAQFormView.as_view()(request)
        self.assertTemplateUsed('faq_specialist_form.html')

    def test_faq_form_has_context_data(self):
        request = self.factory.get(reverse('faq_form_view'))
        request.user = self.specialist
        response = FAQFormView.as_view()(request)
        self.assertTrue('form' in response.context_data)

    def test_faq_form_submission_is_limited_to_specialists(self):
        request = self.factory.post(
            reverse('faq_form_view'), data=self.form_data
        )
        request.user = AnonymousUser()
        response = FAQFormView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FAQ.objects.count(), 1)
