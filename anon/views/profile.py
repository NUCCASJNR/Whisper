#!/usr/bin/env python3

"""Contains view for displaying users profile"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from anon.serializers.profile import ProfileSerializer, ReadyToChatSerializer, MainUser
from rest_framework.response import Response
from rest_framework import status


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
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


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

        option = request.data.get('Option')
        current_user = request.user
        MainUser.custom_update(filter_kwargs={'id': current_user.id},
                               update_kwargs={'ready_to_chat': option})
        return Response({
            'message': 'Status Successfully Updated',
            'status': status.HTTP_200_OK
        })
