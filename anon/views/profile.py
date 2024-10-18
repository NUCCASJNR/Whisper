#!/usr/bin/env python3

"""Contains view for displaying users profile"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from anon.models.key import PublicKeyDirectory
from anon.serializers.profile import MainUser, ObjectDoesNotExist, ProfileSerializer
from anon.utils.key import hash_pin
from rest_framework.exceptions import PermissionDenied


class ProfileView(APIView):
    """User Profile View"""

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request):
        """
        Get request handler
        :param request: Request object
        :return: User profile
        """
        username = request.data.get("username")
        if username != request.user.username:
            raise PermissionDenied("You are only allowed to view your own profile.")
        serializer = self.serializer_class(request.user)
        print(serializer)
        return Response({
            'data': serializer.data,
            "status": status.HTTP_200_OK})


class ReadyToChatView(APIView):
    """
    Ready to chat view
    """

    permission_classes = [IsAuthenticated]
    # serializer_class = ReadyToChatSerializer

    def post(self, request):
        """
        Post request for handling ReadyToChat toggle
        :param request: Request obj
        :return: None
        """

        option = request.data.get("Option")
        current_user = request.user
        MainUser.custom_update(
            filter_kwargs={"id": current_user.id},
            update_kwargs={"ready_to_chat": option},
        )
        return Response(
            {"message": "Status Successfully Updated", "status": status.HTTP_200_OK}
        )


class CreatePinView(APIView):
    """
    View for creating pin for a user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Creates a pin for a user
        Args:
            request: request object
            return: 200 if successful else 400
        """
