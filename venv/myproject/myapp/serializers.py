from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, Volunteer

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='username')
    time = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['username', 'text', 'time']

    def get_time(self, obj):
        return obj.timestamp.strftime('%H:%M')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class VolunteerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Volunteer
        fields = ['user']
