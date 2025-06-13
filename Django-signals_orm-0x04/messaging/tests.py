from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

# Create your tests here.
class MessageNotificationTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='123')
        self.receiver = User.objects.create_user(username='receiver', password='123')

    def test_notification_created_on_message(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hi there!')
        notification = Notification.objects.filter(user=self.receiver, message=message).first()
        self.assertIsNotNone(notification)
        self.assertFalse(notification.is_read)
