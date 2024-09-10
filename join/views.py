from django.db import IntegrityError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from join.models import Task, Team, User
from .serializers import (
    EmailAuthTokenSerializer,
    TaskReadSerializer,
    TaskSerializer,
    UserSerializer,
)
from django.contrib.auth import logout
from django.db.models import Q
import logging
from .utils import *

User = get_user_model()


class LoginView(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        This function gets the user data and returns it in case the user signs in.
        """
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
    """
    This function creates a new user and a new team for the user.
    """
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        user_color = request.data.get("icon")

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
        """
        This function signs out the user.
        """
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


class TeamView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        This function returns the team of the user.
        """
        team = Team.objects.filter(owner=request.user).first()

        if not team:
            return Response(
                {"error": "Team not found or you do not have permission to view it."},
                status=status.HTTP_404_NOT_FOUND,
            )

        members = team.members.all()

        serializer = UserSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        This function removes deletes a user from a team. It calls functions to remove the user from the team and from all the tasks the user is assigned to.
        """
        response = self.remove_member_from_team(request)
        if response.status_code != status.HTTP_200_OK:
            return response

        response = self.remove_member_from_task(request)
        return response

    def remove_member_from_team(self, request):
        team = get_team(request)
        if isinstance(team, Response):
            return team

        user_id = get_user_id(request)
        if isinstance(user_id, Response):
            return user_id

        user_to_add = get_user_by_id(user_id)
        if isinstance(user_to_add, Response):
            return user_to_add

        team.members.remove(user_to_add)
        return Response(
            {"message": "User removed from the team successfully."},
            status=status.HTTP_200_OK,
        )

    def remove_member_from_task(self, request):
        tasks = Task.objects.filter(author=request.user)

        if not tasks.exists():
            return Response(
                {"message": "No tasks found for the user."}, status=status.HTTP_200_OK
            )

        user_id = get_user_id(request)
        if isinstance(user_id, Response):
            return user_id

        user_to_remove = get_user_by_id(user_id)
        if isinstance(user_to_remove, Response):
            return user_to_remove

        for task in tasks:
            task.assignedTo.remove(user_to_remove)

        return Response(
            {"message": "User removed from the task successfully."},
            status=status.HTTP_200_OK,
        )


class AddMemberView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        This function returns all users.
        """
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        This function adds a user to a team.
        """
        team = get_team(request)
        if isinstance(team, Response):
            return team

        user_id = get_user_id(request)
        if isinstance(user_id, Response):
            return user_id

        user_to_add = get_user_by_id(user_id)
        if isinstance(user_to_add, Response):
            return user_to_add

        team.members.add(user_to_add)
        
        return Response(
            {"message": "User added to the team successfully."},
            status=status.HTTP_200_OK,
        )


class AddTaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        """
        This function creates a new task.
        """
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        This function gets all the tasks the user is owner of or is assigend to.
        """
        user = self.request.user
        return get_tasks(user)

    def patch(self, request):
        """
        This function updates a task with a given ID.
        """
        task_id = get_task_id(request)
        if isinstance(task_id, Response):
            return task_id

        try:
            task_to_update = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(task_to_update, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            serializerResponse = TaskReadSerializer(task_to_update)
            return Response(serializerResponse.data, status=status.HTTP_200_OK)
        else:
            logging.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        This function deletes a task with a given ID.
        """
        user = self.request.user

        task_id = get_task_id(request)
        if isinstance(task_id, Response):
            return task_id

        task_to_delete = Task.objects.filter(id=task_id, author=user).first()
        if not task_to_delete:
            return Response(
                {"error": "Task not found or you don't have permission to delete it."},
                status=status.HTTP_404_NOT_FOUND,
            )

        task_to_delete.delete()

        return get_tasks(user)
    
def get_tasks(user):
    tasks = Task.objects.filter(Q(author=user) | Q(assignedTo=user)).distinct()
    serializer = TaskReadSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

