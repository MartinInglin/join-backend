from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from join.models import Team, User
from .serializers import EmailAuthTokenSerializer, UserSerializer
from django.contrib.auth import logout


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
                {
                    "token": token.key,
                    "user_id": user.pk,
                    "email": user.email,
                    "color": user.user_color,
                    "name": user.username,
                }
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
        user_color = request.data.get("icon")

        User = get_user_model()

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password, user_color=user_color
            )
            self.create_team(user)
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response(
                {"error": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create_team(self, user):
        team = Team.objects.create(owner=user)
        team.members.add(user)


class LogoutView(APIView):
    permission_classes = []

    def post(self, request):
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )
    
class TeamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        team = Team.objects.filter(owner=request.user).first()

        if not team:
            return Response(
                {"error": "Team not found or you do not have permission to view it."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        members = team.members.all()

        serializer = UserSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
