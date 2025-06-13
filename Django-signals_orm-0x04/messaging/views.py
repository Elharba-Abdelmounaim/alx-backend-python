from django.shortcuts import render
from .models import Message

def threaded_conversations(request):
    messages = Message.objects.filter(parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies')

    return render(request, 'messaging/threaded_conversations.html', {'messages': messages})
