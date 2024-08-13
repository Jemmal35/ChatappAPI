# serializers.py
from rest_framework import serializers
from .models import ChatRoom, Message, DirectMessage, Notification

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'room', 'content', 'timestamp']
        read_only_fields = ['user', 'timestamp']

class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'receiver', 'content', 'is_seen', 'timestamp']
        read_only_fields = ['sender', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']
