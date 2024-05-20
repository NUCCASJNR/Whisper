#!/usr/bin/env python3

"""Contains Authentication related views"""

from rest_framework import status
from rest_framework import viewsets, views
from rest_framework.response import Response
from anon.utils.task import generate_key_async
from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from anon.serializers.auth import (
    MainUser,
    SignUpSerializer,
    LoginSerializer
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
                'id': user.id,
                'status': status.HTTP_201_CREATED
            })
        return Response({
            'error': serializer.errors,
            'status': status.HTTP_400_BAD_REQUEST
        })


class LoginView(views.APIView):
    """
    View for logging in a user
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Post request Handler
        :param request: Request obj
        :param args: Args
        :param kwargs: Keyword Args
        :return: 200 or 400
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.initial_data)
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "You have successfully logged in",
                    "access_token": str(refresh.access_token),
                    "status": status.HTTP_200_OK,
                })
            return Response({
                'error': 'Invalid username or password',
                'status': status.HTTP_400_BAD_REQUEST
            })
        return Response({
            'error': serializer.errors,
            'status': status.HTTP_400_BAD_REQUEST
        })


class LogoutView(views.APIView):
    """
    View to lougout a user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Post request handler
        :param request: Request obj
        :param args:Arg
        :param kwargs: Keyword Args
        :return: 200 or 400
        """
        try:
            refresh_token = request.headers['Authorization']
            print(f'refresh: {refresh_token}')
        except KeyError:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProtectedRoute(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'message': 'You are authenticated'}, status=status.HTTP_200_OK)