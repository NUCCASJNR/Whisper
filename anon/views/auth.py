#!/usr/bin/env python3

"""Contains Authentication related views"""

from rest_framework import status
from rest_framework import viewsets, views
from rest_framework.response import Response
from anon.utils.task import generate_key_async
from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from anon.serializers.auth import (
    MainUser,
    SignUpSerializer
)


class SignUpViewSet(viewsets.ModelViewSet):
    """
    This view handles user signup
    """

    serializer_class = SignUpSerializer
    queryset = MainUser.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Creates a new user
        :param request: Request arg
        :param args: ARgs e.g serializer validated datas
        :param kwargs: Keyword Args
        :return: 201 or 400
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = MainUser.custom_save(**serializer.validated_data)
            generate_key_async(user.id)
            return Response({
                'message': 'Signup successful, You can now login',
                'status': status.HTTP_201_CREATED
            })
        return Response({
            'error': serializer.error_messages,
            'status': status.HTTP_400_BAD_REQUEST
        })


class LoginView(views.APIView):
    """
    View for logging in a user
    """