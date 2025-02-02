from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Conversation
from .serializers import ConversationSerializer


from staff.models import Staff
from client.models import CompanyProfile 
from users.models import User

# get chat messages
class ConversationsAPI(APIView):
    
    def get(self, request, pk=None):
        messages = Conversation.objects.filter(Q(sender=request.user) and Q(receiver_id=pk))
        serializer = ConversationSerializer(messages, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk=None):
        data = request.data
        sender = request.user
        receiver = User.objects.filter(id=pk).first()
        if not receiver:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        conversation = Conversation.objects.create(sender=sender, receiver=receiver, message= data['message'])
        response_data = {
            "status": status.HTTP_200_OK,
            "message": "Message sent successfully",
            "data": ConversationSerializer(conversation).data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    