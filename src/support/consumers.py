import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime





class ChatSupportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f"support_chat_{self.session_id}"

        # Присоединяем пользователя к группе WebScoket
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Удаляем пользователя из группы WebSocket
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        from support.models import ChatSupportSession, ChatSupportMessage
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender'].title()
        timestamp = data['timestamp']

        # Сохраняем сообщение в базе данных
        session = await sync_to_async(ChatSupportSession.objects.get)(id=self.session_id)
        await sync_to_async(ChatSupportMessage.objects.create)(
            session=session,
            sender=sender,
            content=message,
        )

        # Отправляем сообщение в группу WebSocket
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
                "timestamp": timestamp
            }
        )

    async def chat_message(self, event):
        # Отправляем сообщение клиенту
        await self.send(
            text_data=json.dumps(
                {
                    "message": event['message'],
                    "sender": event['sender'],
                    "timestamp": event['timestamp'],
                }))
