from django.http import HttpRequest
from rest_framework.permissions import BasePermission

class IsAgent(BasePermission):
    """
    Custom permission to only allow access to agents.
    """
    def has_permission(self, request: HttpRequest, view):
        if request.user.is_authenticated:
            return hasattr(request.user, "agent")
        return False