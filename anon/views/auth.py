#!/usr/bin/env python3

"""Contains Authentication related views"""

from django.contrib.auth import authenticate, login
from rest_framework import status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from anon.serializers.auth import LoginSerializer, MainUser, SignUpSerializer
from anon.utils.task import generate_key_async



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
            refresh_token = request.headers["Authorization"]
            print(f"refresh: {refresh_token}")
        except KeyError:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FindUserView(views.APIView):
    """
    View for finding a user
    """
    def post(self, request):
        try:
            user = MainUser.find_obj_by(**{"username": request.data.get("username")})
            if user:
                return Response({
                    "message": "User Found!!",
                    "status": 200
                })
            else:
                return Response({
                    "error": "No such user",
                    "status": 404
                })
        except ValueError:
            return Response({
                "error": "No such user",
                "status": 404
            })
