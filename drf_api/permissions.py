from rest_framework import permissions
from profiles.models import Profile
from jobs.models import Application, Job
from django.shortcuts import get_object_or_404


class IsOwnerReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsNotificationOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a notification to access it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Return True if the user is the owner of the notification, False otherwise.
        """
        return obj.owner == request.user


class IsNotOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner != request.user


class IsRatingCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class IsEmployerProfile(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        # Check if the user is authenticated before accessing the profile attribute
        return request.user.is_authenticated and request.user.profile.profile_type == 'employer'


class IsEmployeeProfile(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.profile_type == 'employee'


class IsApplicant(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only allow employees (applicants) to apply for jobs
        return request.user.profile.profile_type == 'employee'

    def has_object_permission(self, request, view, obj):
        # Allow applicants to view job details regardless of whether they have applied
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET requests (viewing job details)

        # Ensure obj is a Job instance
        if isinstance(obj, Job):
            # Employees (applicants) can only apply once to a job
            return not Application.objects.filter(job=obj, applicant=request.user.profile).exists()
        return False  # Deny permission if obj is not a Job instance


class IsOwnerOrSender(permissions.BasePermission):
    """
    Custom permission to only allow owners or senders of the chat to view, update, or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the chat or the sender of the message
        return obj.sender == request.user or obj.recipient == request.user


class HasProfileType(permissions.BasePermission):
    """
    Custom permission to only allow users with a profile type to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has a profile type
        return request.user.is_authenticated and request.user.profile_type
