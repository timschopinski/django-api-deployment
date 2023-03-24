from rest_framework import serializers

from .models import Event
from .validators import EventExistsValidator


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class NotificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    event_id = serializers.IntegerField(validators=[EventExistsValidator()])
    send_at = serializers.DateTimeField()
