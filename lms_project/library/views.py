"""
Library Management API Views Module

This module defines the REST API views for managing a library system, including:

- Books: CRUD operations and search/filter functionality.
- Authors: CRUD operations for authors.
- Genres: CRUD operations for genres.
- Borrow Requests: Create, view, approve, reject, and return borrow requests.
- Book Reviews: List and create reviews for books.

Permissions:
- Only authenticated users can view resources.
- Only librarians can create, update, or delete books, authors, genres, and approve/reject borrow requests.

Throttling:
- Borrow requests are throttled using BorrowThrottle to limit request rate per user.
"""

from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now

from library.models import Book, Author, Genre, BorrowRequest, BookReview
from library.serializers import (
    BookSerializer,
    BookCreateSerializer,
    AuthorSerializer,
    GenreSerializer,
    BorrowSerializer,
    ReviewSerializer,
)
from library.permissions import IsLibrarian
from library.throttles import BorrowThrottle


# BOOKS
class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing books.

    Provides CRUD operations for books. Only librarians can create, update, or delete books.
    Users can view and list books.
    """

    queryset = Book.objects.all()
    filterset_fields = ["author", "genres"]
    search_fields = ["title"]
    ordering_fields = ["title", "available_copies"]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on request method.

        **Returns:**
            BookCreateSerializer for POST/PUT requests.
            BookSerializer for other requests.
        """
        if self.request.method in ["POST", "PUT"]:
            return BookCreateSerializer
        return BookSerializer

    def get_permissions(self):
        """
        Returns the permissions for the view based on request method.

        **Returns:**
            IsLibrarian for POST, PUT, DELETE.
            IsAuthenticated for other requests.
        """
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsLibrarian()]
        return [IsAuthenticated()]


# AUTHORS
class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing authors.

    Allows listing and viewing authors for authenticated users.
    Only librarians can create new authors.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        """
        Returns the permissions for the view based on request method.

        **Returns:**
            IsLibrarian for POST requests.
            IsAuthenticated for other requests.
        """
        if self.request.method == "POST":
            return [IsLibrarian()]
        return [IsAuthenticated()]


# GENRES
class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing genres.

    Allows listing and viewing genres for authenticated users.
    Only librarians can create new genres.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        """
        Returns the permissions for the view based on request method.

        **Returns:**
            IsLibrarian for POST requests.
            IsAuthenticated for other requests.
        """
        if self.request.method == "POST":
            return [IsLibrarian()]
        return [IsAuthenticated()]


# BORROW
class BorrowViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing borrow requests.

    Users can create borrow requests and view their own requests.
    Librarians can approve or reject borrow requests.
    """

    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [BorrowThrottle]

    def get_queryset(self):
        """
        Returns borrow requests for the currently authenticated user.

        **Returns:**
            QuerySet of BorrowRequest objects filtered by user.
        """
        return BorrowRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Saves a new borrow request for the authenticated user.

        **Args:**
            - serializer: The serializer instance used for validation.
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"], permission_classes=[IsLibrarian])
    def approve(self, request, pk=None):
        """
        Approve a borrow request. Only accessible by librarians.

        **Args:**
            - request: The HTTP request object.
            - pk: Primary key of the borrow request.

        **Returns:**
            Response with a success message.
        """
        obj = self.get_object()
        obj.status = "APPROVED"
        obj.approved_at = now()
        obj.book.save()
        obj.save()
        return Response({"msg": "Approved"})

    @action(detail=True, methods=["patch"], permission_classes=[IsLibrarian])
    def reject(self, request, pk=None):
        """
        Reject a borrow request. Only accessible by librarians.

        **Args:**
            - request: The HTTP request object.
            - pk: Primary key of the borrow request.

        **Returns:**
            Response with a success message.
        """
        obj = self.get_object()
        obj.status = "REJECTED"
        obj.save()
        return Response({"msg": "Rejected"})

    @action(detail=True, methods=["patch"])
    def return_book(self, request, pk=None):
        """
        Mark a borrow request as returned.

        **Args:**
            - request: The HTTP request object.
            - pk: Primary key of the borrow request.

        **Returns:**
            Response with a success message.
        """
        obj = self.get_object()
        obj.status = "RETURNED"
        obj.returned_at = now()
        obj.book.save()
        obj.save()
        return Response({"msg": "Returned"})


# REVIEWS
class ReviewView(generics.ListCreateAPIView):
    """
    API view for listing and creating book reviews.

    Users can list all reviews for a specific book and add new reviews.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns all reviews for the given book.

        **Returns:**
            QuerySet of BookReview objects filtered by book_id.
        """
        return BookReview.objects.filter(book_id=self.kwargs["book_id"])

    def perform_create(self, serializer):
        """
        Saves a new review for the authenticated user and book.

        **Args:**
            - serializer: The serializer instance used for validation.
        """
        serializer.save(user=self.request.user, book_id=self.kwargs["book_id"])
