# messaging/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory

class MessageEditSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.user2 = User.objects.create_user(username='user2')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello')

    def test_edit_creates_history(self):
        self.message.content = 'Hello, again!'
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, 'Hello')
