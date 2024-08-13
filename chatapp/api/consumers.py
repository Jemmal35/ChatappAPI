# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from .serializers import MessageSerializer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Save message to the database
        room = await database_sync_to_async(ChatRoom.objects.get)(id=self.room_id)
        message = await database_sync_to_async(Message.objects.create)(
            user=self.scope['user'],
            room=room,
            content=message_content
        )

        # Serialize the message
        serializer = MessageSerializer(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': serializer.data
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
