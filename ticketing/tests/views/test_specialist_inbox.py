from django.test import TestCase, Client
from django.urls import reverse
from ticketing.models.users import User


class SpecialistInboxViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('specialist_dashboard')
        User.objects.create_user(
            email='johndoe@example.com',
            first_name='John',
            last_name='Doe',
            password='Password@123',
            role='SP',
        )

    def test_adult_hub_url(self):
        self.assertEqual(self.url, '/specialist_dashboard/')
