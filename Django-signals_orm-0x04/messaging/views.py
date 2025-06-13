from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
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

@cache_page(60)  # 60 ثانية
def messages_list(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    return render(request, 'messages_list.html', {'messages': messages})

# إذا كان View عبارة عن كلاس (class-based view) مثلاً ListView:

from django.views.generic import ListView

@method_decorator(cache_page(60), name='dispatch')
class MessagesListView(ListView):
    model = Message
    template_name = 'messages_list.html'
    
    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')