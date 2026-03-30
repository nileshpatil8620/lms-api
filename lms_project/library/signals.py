"""
Module: library.signals

This module contains signal handlers for the Library Management System (LMS).

- handle_borrow_request: Updates book availability and sends email notifications
  when the status of a BorrowRequest changes.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from library.models import BorrowRequest


@receiver(post_save, sender=BorrowRequest)
def handle_borrow_request(
    sender, instance: BorrowRequest, created: bool, **kwargs
) -> None:
    """
    Signal handler for BorrowRequest post_save.

    Updates the available_copies of the associated Book when a borrow request
    is approved or returned. Sends email notifications to the user when the
    status changes to APPROVED or REJECTED.

    **Args:**
        - sender (type): The model class that sent the signal (BorrowRequest).
        - instance (BorrowRequest): The BorrowRequest instance that was saved.
        - created (bool): True if a new record was created, False if updated.
        - **kwargs: Additional keyword arguments.

    **Returns:** None
    """
    # Update book copies
    if instance.status == "APPROVED":
        instance.book.available_copies -= 1
        instance.book.save()
    elif instance.status == "RETURNED":
        instance.book.available_copies += 1
        instance.book.save()

    # Send email only if status changed
    if not created:
        old_instance: BorrowRequest = BorrowRequest.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            if instance.status == "APPROVED":
                send_mail(
                    subject="Book Approved",
                    message=f"Your request for {instance.book.title} is approved.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[instance.user.email],
                    fail_silently=False,
                )
            elif instance.status == "REJECTED":
                send_mail(
                    subject="Book Rejected",
                    message=f"Your request for {instance.book.title} is rejected.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[instance.user.email],
                    fail_silently=False,
                )
