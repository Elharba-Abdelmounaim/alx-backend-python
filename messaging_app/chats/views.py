from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.AllowAny] 

    def perform_create(self, serializer):
       
        serializer.save()

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """إرسال رسالة داخل محادثة محددة"""
        conversation = self.get_object()
        sender = request.user 
        content = request.data.get('content')

        if not content:
            return Response({"error": "Content is required."}, status=400)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=content
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny] 

    def perform_create(self, serializer):
       
        serializer.save(sender=self.request.user)
