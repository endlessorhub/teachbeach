from rest_framework import filters
from django.db.models import Q


class MessageUserFilter(filters.BaseFilterBackend):
    """
    Filter that only allows users to see objects associated with their account.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(author=request.user) | Q(to_user=request.user))


class UserFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(user=request.user))
