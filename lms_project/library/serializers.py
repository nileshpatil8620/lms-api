"""
Module: library.serializers

This module defines serializers for the Library Management System (LMS) models.

Serializers included:
- AuthorSerializer: For Author model
- GenreSerializer: For Genre model
- BookSerializer: For Book model (nested author and genres)
- BookCreateSerializer: For creating Book instances
- BorrowSerializer: For BorrowRequest model
- ReviewSerializer: For BookReview model
"""

from rest_framework import serializers
from library.models import Author, Genre, Book, BorrowRequest, BookReview


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Serializes all fields of an Author instance.
    """

    class Meta:
        model = Author
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Genre model.

    Serializes all fields of a Genre instance.
    """

    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model with nested author and genres.

    Attributes:
        - author (AuthorSerializer): Nested read-only author details
        - genres (GenreSerializer): Nested read-only list of genres
    """

    author: AuthorSerializer = AuthorSerializer(read_only=True)
    genres: list[GenreSerializer] = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Book instances.

    All fields are writable.
    """

    class Meta:
        model = Book
        fields = "__all__"


class BorrowSerializer(serializers.ModelSerializer):
    """
    Serializer for BorrowRequest model.

    Attributes:
        - status: Read-only status field
        - user: Read-only user field (set automatically)
    """

    class Meta:
        model = BorrowRequest
        fields = "__all__"
        read_only_fields = ["status", "user"]


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for BookReview model.

    Attributes:
        - user: Read-only field (set automatically)
        - book: Read-only field (set automatically)
    """

    class Meta:
        model = BookReview
        fields = "__all__"
        read_only_fields = ["user", "book"]
