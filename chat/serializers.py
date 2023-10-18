from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
