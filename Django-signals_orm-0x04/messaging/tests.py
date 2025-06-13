# messaging/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class UserDeletionTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender')
        self.receiver = User.objects.create_user(username='receiver')
        self.message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hi")
        self.history = MessageHistory.objects.create(message=self.message, old_content="Old")
        self.notification = Notification.objects.create(user=self.receiver, message=self.message)

    def test_user_deletion_cleans_related_data(self):
        self.sender.delete()
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessageHistory.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
