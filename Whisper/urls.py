"""Whisper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path

# from anon.views.message import MessageView, ReceiveMessageView
from rest_framework import routers

from anon.views.auth import LoginView, LogoutView, SignUpViewSet
from anon.views.profile import ListUsersReadyToChat, ProfileView, ReadyToChatView

router = routers.DefaultRouter()
router.register("auth/signup", SignUpViewSet, basename="signup")
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("auth/login/", LoginView.as_view()),
    path("auth/logout", LogoutView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("ready-to-chat/", ReadyToChatView.as_view()),
    path("online-users/", ListUsersReadyToChat.as_view()),
    # path('send-message/<str:user_id>/', MessageView.as_view()),
    # path('messages/<str:user_id>/', ReceiveMessageView.as_view())
]
