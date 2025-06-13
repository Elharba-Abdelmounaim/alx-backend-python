from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Message

class ThreadedConversationTest(TestCase):

    def setUp(self):
        # إنشاء مستخدمين
        self.user1 = User.objects.create_user(username='alice', password='password123')
        self.user2 = User.objects.create_user(username='bob', password='password123')

        # إنشاء رسالة أصلية
        self.root_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hi Bob!"
        )

        # إنشاء رد عليها
        self.reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Hi Alice!",
            parent_message=self.root_message
        )

        # عميل Django
        self.client = Client()

    def test_threaded_view_renders_root_messages(self):
        response = self.client.get('/threads/')

        # هل تم تحميل الصفحة بنجاح؟
        self.assertEqual(response.status_code, 200)

        # هل تحتوي الرسائل في السياق على الرسالة الأصلية فقط؟
        messages = response.context['messages']
        self.assertIn(self.root_message, messages)
        self.assertNotIn(self.reply1, messages)  # الرد لا يجب أن يظهر كرسالة رئيسية
