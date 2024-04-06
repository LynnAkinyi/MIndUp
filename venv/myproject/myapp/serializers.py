from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='username')
    time = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['username', 'text', 'time']

    def get_time(self, obj):
        return obj.timestamp.strftime('%H:%M')

