"""
Module: accounts.views

This module contains views and serializers for user authentication and registration
in the Library Management System (LMS). It includes:

- User registration (RegisterView)
- JWT-based login (LoginView) with custom response
- JWT-based logout (LogoutView) with token blacklisting
"""

from rest_framework import generics, status
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from typing import Any, Dict


class RegisterSerializer(ModelSerializer):
    """
    Serializer for registering new users.

    Handles validation and creation of User instances.

    **Fields:**
        - username: User's username
        - password: User's password
        - role: Role of the user (STUDENT or LIBRARIAN)
    """

    class Meta:
        model = User
        fields = ["username", "password", "role"]

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Create a new user instance using the validated data.

        **Args:**
            - validated_data (dict): Validated serializer data.

        **Returns:**
            - User: Newly created User object.
        """
        return User.objects.create_user(**validated_data)


class RegisterView(generics.CreateAPIView):
    """
    API view for registering new users.

    Uses RegisterSerializer to handle POST requests.
    """

    serializer_class = RegisterSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for JWT token obtain endpoint.

    Adds additional user information to the token response.
    """

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user credentials and return JWT tokens with extra user info.

        **Args:**
            - attrs (dict): Input credentials (username & password).

        **Returns:**
            - dict: JWT tokens along with user_id, username, and role.
        """
        data = super().validate(attrs)
        data.update(
            {
                "user_id": self.user.id,
                "username": self.user.username,
                "role": self.user.role,
            }
        )
        return data


class LoginView(TokenObtainPairView):
    """
    API view for user login (JWT-based).

    Returns access and refresh tokens along with user information.
    """

    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    """
    API view for logging out users by blacklisting the refresh token.

    Requires the user to be authenticated.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Any) -> Response:
        """
        Handle POST request to logout user.

        **Expects:**
            - refresh (str): The JWT refresh token to blacklist.

        **Returns:**
            - Response: Success or error message.
        """
        try:
            refresh_token: str = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
