from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='username')
    time = serializers.DateTimeField(source='timestamp')

    class Meta:
        model = Message
        fields = ['username', 'text', 'time']

