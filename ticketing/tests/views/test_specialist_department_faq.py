from django.test import TestCase
from django.urls import reverse
from ticketing.models import FAQ, Department, User
from django.utils.text import slugify
from ticketing.views.specialist_department_faq import SpecialistDepartmentFaq


class SpecialistDepartmentFaqTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name='Health and Safety', slug=slugify('Health and Safety')
        )
        self.specialist = User.objects.create_specialist(
            email='john.doe@email.com',
            first_name='John',
            last_name='Doe',
            password='password@123',
        )
        self.faq = FAQ.objects.create(
            department=self.department,
            specialist=self.specialist,
            questions='What is 9+10',
            answer='19',
        )
        self.slug_string = slugify('Health and Safety')
        self.url = reverse(
            'department_faq', kwargs={'department': self.department.slug}
        )

    def test_faq_slug(self):
        slugged_string = slugify('Mitigating Circumstances')
        department = Department.objects.create(
            name='Mitigating Circumstances',
            slug=slugify('Mitigating Circumstances'),
        )
        self.assertEquals(slugged_string, department.slug)
        self.assertEquals(self.slug_string, self.faq.department.slug)

    def test_specialist_department_faq_url_resolves(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_specialist_department_faq_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'department_faq.html')
        self.assertTemplateUsed(response, 'partials/header.html')
        self.assertTemplateUsed(response, 'partials/pagination.html')
        self.assertTemplateUsed(response, 'partials/footer.html')

    def test_specialist_department_faq_uses_correct_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.faq.questions,
            [faq.questions for faq in response.context['object_list']],
        )
        self.assertIn(
            self.faq.answer,
            [faq.answer for faq in response.context['object_list']],
        )

    def test_specialist_department_faq_view_contains_question_answer_text(
        self,
    ):
        response = self.client.get(self.url)
        self.assertContains(response, 'What is 9+10')
        self.assertContains(response, '19')

    def test_specialist_department_faq_view_contains_answer_text(self):
        response = self.client.get(self.url)
        self.assertContains(response, '19')

    def test_specialist_department_faq_view_no_pagination(self):
        url = reverse(
            'department_faq', kwargs={'department': self.department.slug}
        )
        response = self.client.get(url)
        self.assertEqual(len(response.context['object_list']), 1)
        FAQ.objects.create(
            department=self.department,
            specialist=self.specialist,
            questions='Why am I tired?',
            answer='Get some sleep',
        )
        url = reverse(
            'department_faq', kwargs={'department': self.department.slug}
        )
        response = self.client.get(url)
        self.assertEqual(len(response.context['object_list']), 2)
        FAQ.objects.get(questions='Why am I tired?').delete()
        url = reverse(
            'department_faq', kwargs={'department': self.department.slug}
        )
        response = self.client.get(url)
        self.assertEqual(len(response.context['object_list']), 1)

    def test_specialist_department_faq_view_get_queryset(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        queryset = response.context_data['object_list']
        self.assertQuerysetEqual(
            queryset,
            FAQ.objects.filter(department=self.department).order_by('id'),
        )
