from django.db import models
from django.conf import settings
from User.models import *

class Room(models.Model):
    class Meta:
        app_label = "chat"
        managed = True
    customer = models.ForeignKey(MyAuthor, related_name='custs_room', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=250)
    manager = models.ForeignKey(MyAuthor, related_name='managers_room', on_delete=models.CASCADE)

class Chat(models.Model):
    class Meta:
        app_label = "chat"
        managed = True
    class SenderType(models.TextChoices):
        server = 'SERVER'
        Client = 'CLIENT'
    sender_id = models.ForeignKey(MyAuthor, related_name='send_chats', on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=250)
    sender_type= models.CharField(max_length=6, choices=SenderType.choices,default= 'SERVER', null=True)
    room = models.ForeignKey(Room,related_name="messages",on_delete=models.CASCADE,null= True , default= None)

