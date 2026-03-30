"""
Module: library.models

This module defines the core models for the Library Management System (LMS),
including authors, genres, books, borrow requests, and book reviews.
"""

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # Type: str


class Author(models.Model):
    """
    Model representing an author.

    **Attributes:**
        - name (str): Full name of the author.
        - bio (str | None): Short biography of the author (optional).
    """

    name: str = models.CharField(max_length=255)
    bio: str | None = models.TextField(blank=True, null=True)


class Genre(models.Model):
    """
    Model representing a book genre.

    **Attributes:**
        - name (str): Name of the genre.
    """

    name: str = models.CharField(max_length=100)


class Book(models.Model):
    """
    Model representing a book.

    **Attributes:**
        - title (str): Title of the book.
        - author (Author): Foreign key to the book's author.
        - genres (QuerySet[Genre]): Many-to-many relationship with genres.
        - isbn (str): ISBN number of the book.
        - available_copies (int): Number of copies currently available.
        - total_copies (int): Total number of copies in the library.
    """

    title: str = models.CharField(max_length=255)
    author: Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    isbn: str = models.CharField(max_length=20)
    available_copies: int = models.IntegerField()
    total_copies: int = models.IntegerField()


class BorrowRequest(models.Model):
    """
    Model representing a book borrow request.

    **Attributes:**
        - book (Book): The book being requested.
        - user (User): The user who requested the book.
        - status (str): Current status of the request ("PENDING", "APPROVED", "REJECTED", "RETURNED").
        - requested_at (datetime): Timestamp when the request was created.
        - approved_at (datetime | None): Timestamp when the request was approved (optional).
        - returned_at (datetime | None): Timestamp when the book was returned (optional).
    """

    STATUS: tuple[tuple[str, str], ...] = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("RETURNED", "Returned"),
    )

    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    status: str = models.CharField(max_length=20, choices=STATUS, default="PENDING")
    requested_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    approved_at: models.DateTimeField | None = models.DateTimeField(
        null=True, blank=True
    )
    returned_at: models.DateTimeField | None = models.DateTimeField(
        null=True, blank=True
    )


class BookReview(models.Model):
    """
    Model representing a review for a book.

    **Attributes:**
        - user (User): User who wrote the review.
        - book (Book): Book being reviewed.
        - rating (int): Rating given by the user (e.g., 1-5).
        - comment (str): Review comment.
        - created_at (datetime): Timestamp when the review was created.
    """

    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating: int = models.IntegerField()
    comment: str = models.TextField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
