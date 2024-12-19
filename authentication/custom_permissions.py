from rest_framework.permissions import BasePermission
from user.models import Tenant, LandLord, Agent

class IsTenant(BasePermission):
    """
    Custom permission to only allow access to tenants.
    """
    def has_permission(self, request, view):
        # Check if the user is a Tenant using some logic.
        if request.user.is_authenticated:
            # Ensure the user is an instance of Tenant
            return hasattr(request.user, "tenant")  # If there’s a relationship with a tenant model
        return False

class IsLandLord(BasePermission):
    """
    Custom permission to only allow access to landlords.
    """
    def has_permission(self, request, view):
        # Check if the user is a LandLord based on username or other attributes
        if request.user.is_authenticated:
            # Check for LandLord relationship or some attribute indicating they are a landlord
            return hasattr(request.user, "landlord")  # E.g., checking a field or model relationship
        return False

class IsAgent(BasePermission):
    """
    Custom permission to only allow access to agents.
    """
    def has_permission(self, request, view):
        # Check if the user is an Agent based on username or attributes
        if request.user.is_authenticated:
            # Ensure the user is an instance of Agent or has the "agent" attribute
            return hasattr(request.user, "agent")  # E.g., checking a field or model relationship
        return False

class IsAgentOrLandLord(BasePermission):
    """
    Custom permission to allow access to either agents or landlords.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Check if the user is either an Agent or a LandLord
            return hasattr(request.user, "agent") or hasattr(request.user, "landlord")
        return False
