#!/usr/bin/env python3

"""Contains view for displaying users profile"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from anon.serializers.profile import ProfileSerializer
from rest_framework.response import Response


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

