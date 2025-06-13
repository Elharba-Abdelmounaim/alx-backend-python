from django.shortcuts import render
from .models import Message

def threaded_conversations(request):
    messages = Message.objects.filter(parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies')

    return render(request, 'messaging/threaded_conversations.html', {'messages': messages})

def inbox(request):
    user = request.user
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messaging/inbox.html', {'messages': unread_messages})