from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserModelTests(TestCase):
    def test_create_user_with_bio(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='pass1234', bio='Hello bio!')
        self.assertEqual(user.bio, 'Hello bio!')
        self.assertTrue(user.check_password('pass1234'))
