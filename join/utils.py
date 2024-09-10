from join.models import Team, User
from rest_framework.response import Response
from rest_framework import status


def get_team(request):
    """
    This function returns the team the user is owner of.
    """
    team = Team.objects.filter(owner=request.user).first()
    if not team:
        return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)
    return team


def get_user_id(request):
    """
    This function returns the user ID from the request data.
    """
    user_id = request.data.get("user_id")
    if not user_id:
        return Response(
            {"error": "No user ID provided."}, status=status.HTTP_400_BAD_REQUEST
        )
    return user_id

def get_user_by_id(user_id):
    """
    This function returns the user data by the user ID.
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
def get_task_id(request):
    """
    This function returns the task ID from the request data.
    """
    task_id = request.data.get('id')

    if not task_id:
        return Response(
            {"error": "Task ID is required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    return task_id
