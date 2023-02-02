from django.test import TestCase

from django.urls import reverse

from http import HTTPStatus

from ticketing.tests.utility.seeding import SeededTestCase

class TestDirectorPanel(SeededTestCase):
    def setUp(self):

        super().setUp()



class TestCommandsView(TestDirectorPanel):
    def setUp(self):
        super().setUp()


    def test_first(self):
        print("What here")

        response = self.client.post(reverse("director_panel"))

        self.assertEqual(response.status_code, HTTPStatus.OK)