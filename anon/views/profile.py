#!/usr/bin/env python3

"""Contains view for displaying users profile"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from anon.serializers.profile import ProfileSerializer, MainUser, ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from anon.models.key import PublicKeyDirectory


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
        return Response({
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })


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


class ListUsersReadyToChat(APIView):
    """
    View for listing users that are reday to chat
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all the users that have their ready-to-chat ON
        :param request:
        :return: Public key of the users that are ready to chat
        """
        try:
            # Retrieve all users ready to chat
            users = MainUser.find_objs_by(**{'ready_to_chat': True})
            exclude_user_id = str(request.user.id)
            user_ids = [str(user.id) for user in users if str(user.id) != exclude_user_id]
            public_keys_list = []
            for user_id in user_ids:
                public_keys = PublicKeyDirectory.custom_get(**{'user_id': user_id}).public_keys.values()
                public_keys_list.extend(public_keys)
            return Response({
                "public_keys": public_keys_list,
                "status": status.HTTP_200_OK
            })
        except ObjectDoesNotExist:
            return Response({
                'message': 'Nobody wan follow you talk'
            })
