from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from .serializers import EmailAuthTokenSerializer


class LoginView(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        try:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user_id": user.pk, "email": user.email}
            )
        except IntegrityError:
            return Response(
                {"error": "A database error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        User = get_user_model()

        try:
            User.objects.create_user(username=username, email=email, password=password)
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response(
                {"error": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
