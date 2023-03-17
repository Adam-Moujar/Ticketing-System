from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser
from django.utils.text import slugify
from django.urls import reverse
from ticketing.models.users import User
from ticketing.models.departments import Department, Subsection
from ticketing.models.tickets import Ticket
from ticketing.models.specialist import SpecialistDepartment
from ticketing.views.specialist_subsection_create import SpecialistSubSectionView
from ticketing.tests.helpers import (
    FixtureHelpers,
    reverse_with_next,
    get_tickets,
)

class SerachBarViewTestCase(TestCase):
    fixtures = [
        'ticketing/tests/fixtures/user_fixtures.json',
        'ticketing/tests/fixtures/message_fixtures.json',
        'ticketing/tests/fixtures/ticket_fixtures.json',
        'ticketing/tests/fixtures/department_fixtures.json',
        'ticketing/tests/fixtures/specialist_department_fixtures.json',
        'ticketing/tests/fixtures/subsection_fixtures.json',
        'ticketing/tests/fixtures/faq_fixtures.json'
    ]

    def setUp(self):
        self.specialist = User.objects.get(
            email=(FixtureHelpers.get_specialist_from_fixture())['email']
        )
        self.student = FixtureHelpers.get_student_from_fixture()
        self.director = FixtureHelpers.get_director_from_fixture()
        
        self.departments = FixtureHelpers.get_all_departments_from_fixture()
        self.subsectipns = FixtureHelpers.get_all_subsection_from_fixture()
        self.faqs = FixtureHelpers.get_all_faqs_from_fixture() 

        self.url = reverse(
            'search_bar'
        )
    
    def test_search_bar_url(self):
        self.assertEqual(self.url, '/search_bar/')

    

    