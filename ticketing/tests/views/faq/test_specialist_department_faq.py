from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ticketing.models import FAQ, Department, User, SpecialistDepartment, Subsection, Ticket
from django.utils.text import slugify
from ticketing.views.faq.specialist_department_faq import SpecialistDepartmentFaq
from django.http import Http404
from django.shortcuts import get_object_or_404



class SpecialistDepartmentFaqTestCase(TestCase):

    fixtures = [
        'ticketing/tests/fixtures/user_fixtures.json',
        'ticketing/tests/fixtures/message_fixtures.json',
        'ticketing/tests/fixtures/ticket_fixtures.json',
        'ticketing/tests/fixtures/department_fixtures.json',
        'ticketing/tests/fixtures/specialist_department_fixtures.json',
        'ticketing/tests/fixtures/subsection_fixtures.json',
    ]
    
    def setUp(self):
        self.factory = RequestFactory()
        self.specialist = User.objects.filter(role = 'SP').first()
        self.department = SpecialistDepartment.objects.get(specialist = self.specialist).department
        self.subsection = Subsection.objects.filter(department = self.department).first()
        self.ticket = Ticket.objects.filter(department = self.department).first()
        self.url = reverse('specialist_create_faq_from_ticket',kwargs={"pk":self.ticket.id})
        self.ticket_id = self.ticket.id

        self.faq = FAQ.objects.create(
            specialist=self.specialist,
            subsection=self.subsection,
            department=self.department,
            question='What is the meaning of existence',
            answer='This question cannot be computed... error',
        )
        self.slug_string = slugify(self.department.name)
        self.url = reverse(
            'department_faq', kwargs={'department': self.department.slug}
        )
        self.factory = RequestFactory()

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
        self.assertTemplateUsed(response, 'faq/department_faq.html')
        self.assertTemplateUsed(response, 'partials/header.html')
        self.assertTemplateUsed(response, 'partials/footer.html')

    def test_specialist_department_faq_uses_correct_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.faq.question,
            [faq.question for faq in response.context['object_list']],
        )
        self.assertIn(
            self.faq.answer,
            [faq.answer for faq in response.context['object_list']],
        )

    def test_specialist_department_faq_view_contains_question_answer_text(
        self,
    ):
        response = self.client.get(self.url, follow=True)
        print(response.content)
        self.assertContains(response, 'What is the meaning of existence')
        self.assertContains(response, 'This question cannot be computed... error')


    def test_specialist_department_faq_view_no_pagination(self):
        url = reverse(
            'department_faq', kwargs={'department': self.department.slug}
        )
        response = self.client.get(url)
        self.assertEqual(len(response.context['object_list']), 1)
        FAQ.objects.create(
            department=self.department,
            specialist=self.specialist,
            subsection=self.subsection,
            question='Why am I tired?',
            answer='Get some sleep',
        )
        url = reverse(
            'department_faq', kwargs={'department': self.department.slug}
        )
        response = self.client.get(url)
        self.assertEqual(len(response.context['object_list']), 2)
        FAQ.objects.get(question='Why am I tired?').delete()
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

    def test_specialist_department_faq_view_returns_404_if_no_object_found(
        self,
    ):
        specialist_dept = SpecialistDepartment.objects.get(
            specialist=self.specialist
        ).department
        with self.assertRaises(Http404):
            get_object_or_404(Department, id=specialist_dept.id + 78899)

    def test_specialist_department_faq_view_returns_404_if_object_found(self):
        object = get_object_or_404(Department, id=self.department.id)
        self.assertEqual(object, self.department)

    def test_get_context_data(self):
        request = self.factory.get(self.url)
        request.user = self.specialist
        response = SpecialistDepartmentFaq.as_view()(request)
        self.assertQuerysetEqual(
            response.context_data['object_list'],
            FAQ.objects.filter(specialist=self.specialist),
        )
