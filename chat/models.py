from django.db import models
from django.conf import settings
from User.models import *


class Chat(models.Model):
    class SenderType(models.TextChoices):
        server = 'SERVER'
        Client = 'CLIENT'
    sender_id = models.ForeignKey(MyAuthor, related_name='send_chats', on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=250)
    sender_type= models.CharField(max_length=6, choices=SenderType.choices,default= 'SERVER', null=True)
