from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    bio = models.TextField(blank=True, null=True)
    # Custom user model extending AbstractUser to include a bio field
    # Removed redundant 'User' class to avoid conflicts; use this as the primary user model
    # Configure in settings.py: AUTH_USER_MODEL = 'myapp.CustomUser'

    def __str__(self):
        return self.username
   
    pass


    
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} with {self.participants.count()} participants"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

