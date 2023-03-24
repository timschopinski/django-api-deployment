from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from .serializers import NotificationSerializer
from .tasks import send_event_email_task


class NotificationView(APIView):

    def get_serializer(self):
        return NotificationSerializer()

    @staticmethod
    def post(request: Request) -> HttpResponse:
        email = request.data.get('email')
        event_id = request.data.get('event_id')
        send_at = request.data.get('send_at')
        serializer = NotificationSerializer(data={
            'email': email,
            'event_id': event_id,
            'send_at': send_at,
        })
        serializer.is_valid(raise_exception=True)
        send_at_dt = datetime.strptime(send_at, '%Y-%m-%dT%H:%M:%S.%fZ')

        send_event_email_task.apply_async(
            args=[serializer.validated_data['email'], serializer.validated_data['event_id']], eta=send_at_dt
        )

        return Response({'message': 'Email will be sent at {}'.format(send_at)}, status=status.HTTP_200_OK)
