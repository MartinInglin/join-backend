"""
URL configuration for join_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from join.views import (
    LoginView,
    LogoutView,
    RegisterView,
    TeamView,
    AddMemberView,
    AddTaskView,
    BoardView,
)

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("team/", TeamView.as_view()),
    path("addMember/", AddMemberView.as_view()),
    path("addTask/", AddTaskView.as_view()),
    path("board/", BoardView.as_view()),
]
