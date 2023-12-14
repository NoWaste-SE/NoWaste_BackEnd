# chat/consumers.py
import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync,  sync_to_async
from channels.generic.websocket import WebsocketConsumer
from .models import * 
from User.models import *
from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    # def connect(self,room_name):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_name = room_name
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    # Define a custom function to serialize datetime objects
    def serialize_datetime(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")
  
    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']
        room = data['room_name']
        user = MyAuthor.objects.get(id= user_id)
        async_to_sync(self.save_message)(user, room, message)
        
        date = datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'date' : date
            }
        )


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
        }))

    @sync_to_async
    def save_message(self, user, room, message):
        room_instance = Room.objects.filter(room_name = room).first()
        if (room_instance is None):
            ids= room.split('_')
            custId = ids[0]
            mngId = ids[1]
            customer = MyAuthor.objects.filter(id = custId).first()
            manager = MyAuthor.objects.filter(id= mngId).first()
            room_instance = Room.objects.create(customer = customer , manager = manager, room_name = room)
        # Chat.objects.create(sender_id=user, room_name=room, message=message,room = room_instance.id)
        Chat.objects.create(sender_id=user, room_name=room, message=message)


