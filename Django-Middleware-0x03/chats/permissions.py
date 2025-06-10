# messaging_app/chats/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow users to view and edit only their own messages and conversations.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, or OPTIONS requests (read-only) for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write permissions only if the user is the owner
        # Assumes models have a 'user' field or similar (e.g., 'sender' for Message, 'participants' for Conversation)
        return obj.user == request.user or request.user in obj.participants.all()