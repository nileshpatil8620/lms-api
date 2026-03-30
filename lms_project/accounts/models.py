"""
Module: accounts.models

This module defines the custom User model for the Library Management System (LMS).
The User model extends Django's AbstractUser to include a 'role' field that
distinguishes between students and librarians, and ensures a unique email for each user.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    **Attributes:**
        - role (str): The role of the user in the library system. Can be either
          "STUDENT" or "LIBRARIAN".
        - email (str): Unique email address for the user.
    """

    ROLE_CHOICES: tuple[tuple[str, str], ...] = (
        ("STUDENT", "Student"),
        ("LIBRARIAN", "Librarian"),
    )

    role: str = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        help_text="Role of the user: either Student or Librarian.",
    )
    email: str = models.EmailField(
        unique=True, help_text="Unique email address for the user."
    )
