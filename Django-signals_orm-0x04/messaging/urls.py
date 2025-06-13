from django.urls import path
from .views import threaded_conversations

urlpatterns = [
    path('threads/', threaded_conversations, name='threaded_conversations'),
]
