from django.test import Client, TestCase
from django.urls import reverse
from ticketing.models import User, Ticket, Message, StudentMessage, SpecialistInbox, SpecialistMessage

class SpecialistMessageViewTestCase(TestCase):
    fixtures = [
        'ticketing/tests/fixtures/user_fixtures.json',
        'ticketing/tests/fixtures/message_fixtures.json',
        'ticketing/tests/fixtures/ticket_fixtures.json',
        'ticketing/tests/fixtures/department_fixtures.json',
        'ticketing/tests/fixtures/specialist_department_fixtures.json',
        'ticketing/tests/fixtures/specialist_inbox_fixtures.json',
    ]
    def setUp(self):
        self.specialist = User.objects.filter(role='SP').first()
        self.ticket = SpecialistInbox.objects.filter(specialist = self.specialist).first().ticket
        self.url = reverse('specialist_message', kwargs={'pk' : self.ticket.id})
        self.not_specialist_ticket = SpecialistInbox.objects.exclude(specialist = self.specialist).first().ticket
   
    def test_specialist_message_url(self):
         self.assertEqual(self.url, "/specialist_message/" + str(self.ticket.id) )

    def test_specialist_message_post(self):
        self.client = Client()
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )

        response = self.client.get(self.url, follow=True)
        data = {
            'content': 'Test message content'
        }
        before_count = Message.objects.count()
        self.client.post(self.url, data=data)
        after_count = Message.objects.count()

        self.assertEquals(before_count + 1 , after_count)
        # Check that the message was saved to the database
        specialist_message = SpecialistMessage.objects.filter(
            ticket=self.ticket,
            content='Test message content'
        ).first()
        self.assertIsNotNone(specialist_message)
    
    def test_wrong_pk_when_post(self): 
        self.client = Client()
        self.url = reverse('specialist_message', kwargs={'pk' : self.not_specialist_ticket.pk})
        loggedin = self.client.login(
            email=self.specialist.email, password='Password@123'
        )
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'specialist_dashboard.html')