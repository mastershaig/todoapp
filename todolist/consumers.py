from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
import traceback
from .models import Todolist, Messenger
from django.core.serializers.json import DjangoJSONEncoder

import json



class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['post']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        room = Todolist.objects.filter(id=self.room_name).last()
        self.room = room
        self.data = list(Messenger.objects.filter(todoapp=room).values('pk','user__username', 'content','created_at'))

        print(self.data)
        # Join room group
        if self.user.username and room:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data= json.dumps(
  self.data,
  sort_keys=True,
  indent=1,
  cls=DjangoJSONEncoder
))
        else:
            raise DenyConnection("what the heck bro")

        #

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_obj = Messenger.objects.create(
            user=self.user,
            todoapp=self.room,
            content=message,
        )
        response_data = {
            "pk": message_obj.pk,
            'user_id': message_obj.user.pk,
            "message": message_obj.content,
            "date": message_obj.created_at.strftime("%H:%M %p %Y-%m-%d"),
            "username": self.user.username
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': response_data
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))