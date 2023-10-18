# chat/consumers.py
import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync,  sync_to_async
from channels.generic.websocket import WebsocketConsumer , AsyncWebsocketConsumer
from .models import * 
from User.models import *
from datetime import datetime

# room_name = custId&mngId

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
        sender_id = data['sender_id']
        reciever_id = data['reciever_id']
        room = data['room_name']


        # suser = MyAuthor.objects.get(id= sender_id)
        # ruser = MyAuthor.objects.get(id = reciever_id)
        async_to_sync(self.save_message)(sender_id,reciever_id, room, message)
        # Send message to room group
        date = datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,

                'sender_id':sender_id,
                'reciever_id': reciever_id,

                'date' : date
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        sender_id = event['sender_id']
        reciever_id = event['reciever_id']      
        date = event['date']  
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'reciever_id':reciever_id,
            'date':date
        }))

    @sync_to_async
    def save_message(self, sid,rid, room, message):
        Chat.objects.create(sender_id=sid,reciever_id = rid, room_name=room, message=message)

