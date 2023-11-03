from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import  login_required
import json
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import ChatSerializer
from .models import *
from User.models import *
from django.http import JsonResponse
from django.db.models import Q
from itertools import chain
from rest_framework import serializers

'''Get chat messages of a specific room between a specific customer and manager'''
def room(request,custId,mngId):
    custid = custId
    mngid = mngId
    room_name = f'{custid}_{mngid}'
    messages = Chat.objects.filter(room_name=room_name)
    serializer = ChatSerializer(messages, many=True)
    return HttpResponse(serializer.data,status=status.HTTP_200_OK)

'''Get the names of people who a person has chated with them  '''  
def get_names(request,*args,**kwargs):
    uid = kwargs['user_id'] #get the user id which has send the request
    rcvs = Chat.objects.filter( sender_id=uid).select_related('reciever').all() #the get the recievers which the user was sender of the message
    snds = Chat.objects.filter( reciever_id=uid).select_related('sender').all()    #the senders which the user was sender of the message               
    names = {}
    name = ""
    if rcvs.count()>0 :
        for rcv in rcvs:
            if(rcv.reciever.role == 'customer'):
                try :
                    name = Customer.objects.get(myauthor_ptr_id = rcv.reciever.id).name
                except Exception as E :
                    return HttpResponse("There is not any reciever with the given Id and email {rcv.reciever.email}" , status=status.HTTP_404_NOT_FOUND)
            else:
                try :
                    name = RestaurantManager.objects.get(myauthor_ptr_id = rcv.reciever.id).name
                except Exception as E :
                    return HttpResponse("There is not any reciever with the given Id" , status=status.HTTP_404_NOT_FOUND)
            names[name] = rcv.reciever.id
    if snds.count() >0 :
        for snd in snds:
            if(snd.sender.role == 'customer'):
                try:
                    name = Customer.objects.get(myauthor_ptr_id = snd.sender.id).name
                except Exception as E :
                    return HttpResponse("There is not any sender with the given Id" , status=status.HTTP_404_NOT_FOUND)
            else:
                try :
                    name = RestaurantManager.objects.get(myauthor_ptr_id = snd.sender.id).name
                except Exception as E :
                    return HttpResponse("There is not any sender with the given Id" , status=status.HTTP_404_NOT_FOUND)           
            names[name] = snd.sender.id
    return  HttpResponse( json.dumps( names ) )

# developer API for cleaning database :)
def delete_all_chats(request):
    messages =  Chat.objects.all()
    for ms in messages:
        Chat.objects.filter(id = ms.id).delete()
    return HttpResponse("done",status = status.HTTP_200_OK)
