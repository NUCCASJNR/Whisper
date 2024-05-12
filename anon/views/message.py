from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from anon.serializers.message import MessageSerializer, PlainTextMessage, RecieveMessageSerializer
from anon.models.user import MainUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class MessageView(views.APIView):
    """Message View"""
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, user_id):
        """
        Post request handler
        :param user_id: id of the user to send the message to
        :param request: Request object
        :return: Response object
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            sender = request.user
            if str(sender.id) == user_id:
                return Response({
                    'message': 'You cannot send message to yourself',
                    'status': status.HTTP_400_BAD_REQUEST
                })
            try:
                receipent = MainUser.custom_get(**{'id': user_id})
            except ObjectDoesNotExist:
                return Response({
                    'message': 'User not found',
                    'status': status.HTTP_404_NOT_FOUND
                })
            message = PlainTextMessage.custom_save(sender=sender, recipient=receipent,
                                                   content=serializer.validated_data['content'])
            channel_layer = get_channel_layer()
            room_name = f"chat_{receipent.username}"
            async_to_sync(channel_layer.group_send)(
                room_name, {
                    "type": "chat.message",
                    "message": message.content
                }
            )
            return Response({
                'message': 'Message Sent',
                'status': status.HTTP_200_OK
            })
        return Response({
            'message': serializer.errors,
            'status': status.HTTP_400_BAD_REQUEST
        })


class RecieveMessageView(views.APIView):
    """Receive Message View"""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """
        Get request handler
        :param user_id: id of the user that sent the message
        :param request: Request object
        :return: Response object
        """
        user = request.user
        messages = PlainTextMessage.objects.filter(
            (Q(recipient=user.id) & Q(sender=user_id)) | (Q(recipient=user_id) & Q(sender=user.id))
        ).order_by('-updated_at')

        serializer = RecieveMessageSerializer(messages, many=True)
        return Response(serializer.data)
