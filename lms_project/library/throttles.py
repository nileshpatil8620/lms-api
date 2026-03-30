"""
Module: library.throttles

This module defines custom throttling classes for the Library Management System (LMS).

- BorrowThrottle: Limits the rate at which a user can create borrow requests.
"""

from rest_framework.throttling import UserRateThrottle


class BorrowThrottle(UserRateThrottle):
    """
    Custom throttle for borrow requests.

    **Attributes:**
        - scope (str): The throttle scope, used to configure rate limits in settings.
    """

    scope: str = "borrow"
