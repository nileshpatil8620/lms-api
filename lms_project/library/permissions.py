"""
Module: library.permissions

This module defines custom permissions for the Library Management System (LMS).

- IsLibrarian: Grants access only to users with the librarian role.
- IsOwnerOrReadOnly: Grants full access to the owner of an object and read-only access to others.
"""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from typing import Any


class IsLibrarian(BasePermission):
    """
    Permission class to allow access only to librarians.

    Methods:
        - has_permission: Checks if the requesting user has the 'LIBRARIAN' role.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        Determine if the user has librarian privileges.

        Args:
            request (Request): The HTTP request object.
            view (APIView): The view being accessed.

        Returns:
            bool: True if user.role is 'LIBRARIAN', False otherwise.
        """
        return request.user.role == "LIBRARIAN"


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission class to allow full access to the owner of an object and read-only access to others.

    Methods:
        - has_object_permission: Checks if the requesting user is the object owner or if the request is read-only.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        """
        Determine if the requesting user can perform actions on the object.

        Args:
            request (Request): The HTTP request object.
            view (APIView): The view being accessed.
            obj (Any): The object being accessed.

        Returns:
            bool: True if the user owns the object or the request method is 'GET'.
        """
        return obj.user == request.user or request.method in ["GET"]
