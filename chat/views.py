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
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
from django.db.models import Q
from itertools import chain
from rest_framework import serializers

class ChatViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    @action(
        detail=False,
        methods=['get', 'post'],
        url_path=r'index',
        url_name='chat_index',
        permission_classes=[AllowAny]
    )
    def index(self, request):
        return render(request, 'chat/index.html')
    
    # @action(
    #     detail=True,
    #     methods=['get', 'post'],
    #     url_path=r'room/(?P<room_name>\w+)/user_id/(?P<user_id>\w+)',
    #     url_name='chat_room',
    #     permission_classes=[AllowAny]
    # )
    # def room(self, request, room_name, user_id):
    #     messages = Chat.objects.filter(room=room_name)
    #     print("messssssages22222:")
    #     print (messages)
    #     return render(request, 'chat/room.html', {'room_name': room_name, 'user_id': user_id, 'messages': messages})
    
    @action(
        detail=False,
        methods=['get', 'post'],
        url_path=r'room/messages/(?P<room_name>\w+)',
        url_name='chat_room',
        permission_classes=[IsAuthenticated]
    )
    def get_room_messages(self, request, room_name, *args, **kwargs):
        
        try:
            chats = Chat.objects.filter(room_name=room_name)
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        

    def room(request):
        custid = request.kwargs['custId']
        mngid = request.kwargs['mngId']
        room_name = f'{custid}_{mngid}'
        messages = Chat.objects.filter(room_name=room_name)
        # return render(request, 'chat/room.html', {'room_name': room_name, 'messages': messages})
        return render(request, {'room_name': room_name, 'messages': messages})
def room(request,custId,mngId):
    # custid = request.kwargs['custId']
    # mngid = request.kwargs['mngId']
    custid = custId
    mngid = mngId
    room_name = f'{custid}_{mngid}'
    messages = Chat.objects.filter(room_name=room_name)
    # return render(request, 'chat/room.html', {'room_name': room_name, 'messages': messages})
    # return render(request, {'room_name': room_name, 'messages': messages})
    # return HttpResponse( json.dumps( {'room_name': room_name, 'messages': messages} ) )
    serializer = ChatSerializer(messages, many=True)
    return HttpResponse(serializer.data,status=status.HTTP_200_OK)
    return HttpResponse(data, content_type="application/json")
    
def get_names(request,*args,**kwargs):
    uid = kwargs['user_id']
    rcvs = Chat.objects.filter( sender_id=uid).select_related('reciever').all()
    # print("***************************************************************************8")
    # print(r_names)
    snds = Chat.objects.filter( reciever_id=uid).select_related('sender').all()
    # print("***************************************************************************8")
    # print(s_names)
    # for s in s_names :
    #     print("&&&&&&&&&&&&&&&")
    #     print(s)
    # r_names = r_names.values('name')
    # s_names = s_names.values('name')                    
    names = {}
    name = ""
    print(rcvs)
    print("&&&&&&&&&&&&&&&&&&&&")
    print(snds)
    if rcvs.count()>0 :
        print(rcvs.count())
        print(rcvs)
        for rcv in rcvs:
            if(rcv.reciever.role == 'customer'):
                try :
                    print("*********************************")
                    print(rcv.reciever.id)
                    print(Customer.objects.get(myauthor_ptr_id = rcv.reciever.id))
                    print("****************************")
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
                print("****************************",snd.sender.id)
                try:
                    # print(Customer.objects.get(myauthor_ptr_id = snd.sender.id))
                    name = Customer.objects.get(myauthor_ptr_id = snd.sender.id).name
                except Exception as E :
                    return HttpResponse("There is not any sender with the given Id" , status=status.HTTP_404_NOT_FOUND)
            else:
                try :
                    name = RestaurantManager.objects.get(myauthor_ptr_id = snd.sender.id).name
                except Exception as E :
                    return HttpResponse("There is not any sender with the given Id" , status=status.HTTP_404_NOT_FOUND)           
            names[name] = snd.sender.id
    # names = Chat.objects.filter(Q(sender_id= uid) | Q(reciever_id = uid )).
    return  HttpResponse( json.dumps( names ) )

def delete_all_chats(request):
    messages =  Chat.objects.all()
    for ms in messages:
        Chat.objects.filter(id = ms.id).delete()
    return HttpResponse("done",status = status.HTTP_200_OK)
