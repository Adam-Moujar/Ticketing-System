from django.test import TestCase
from ticketing.models import User, FAQ, Department
from django.utils.text import slugify
from django.urls import reverse


class UpdateFAQFormView(TestCase):
    def setUp(self):
        self.specialist = User.objects.create_specialist(
            email='test.specialist@email.com',
            first_name='test',
            last_name='name',
            password='Password@123',
        )
        self.department = Department.objects.create(
            name='Technology Help', slug=slugify('Technology Help')
        )
        self.faq = FAQ.objects.create(
            department=self.department,
            specialist=self.specialist,
            questions='What is 9+10?',
            subsection='Pain',
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
        self.client.login(email='user@email.com', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_user_with_required_role_can_access_update_faq_view(self):
        self.client.login(
            email='test.specialist@email.com',
            first_name='test',
            last_name='name',
            password='Password@123',
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_submission_redirects_update_faq_view_to_home_page(self):
        self.client.login(
            email='test.specialist@email.com',
            first_name='test',
            last_name='name',
            password='Password@123',
        )
        response = self.client.post(
            self.url,
            {'questions': 'Updated question?','subsection':'Updated Pain', 'answer': 'Updated answer'},
        )
        self.assertRedirects(
            response, reverse('home'), status_code=302, target_status_code=200
        )

    def test_form_submission_updates_faq_object(self):
        self.client.login(
            email='test.specialist@email.com',
            first_name='test',
            last_name='name',
            password='Password@123',
        )
        self.client.post(
            self.url,
            {'questions': 'Updated question?','subsection':'Updated Pain', 'answer': 'Updated answer'},
        )
        updated_faq = FAQ.objects.get(pk=self.faq.pk)
        self.assertEqual(updated_faq.questions, 'Updated question?')
        self.assertEqual(updated_faq.subsection,'Updated Pain')
        self.assertEqual(updated_faq.answer, 'Updated answer')
