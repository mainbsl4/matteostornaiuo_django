from django.shortcuts import render, get_object_or_404
from datetime import date 
from operator import itemgetter

from rest_framework import status, generics 
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .models import  Notification
from . serializers import (
    NotificationSerializer, 
    SkillSerializer,

)

from client.models import CompanyProfile, Vacancy, Job, JobTemplate
from client.serializers import VacancySerializer, JobTemplateSserializers
from staff.models import Staff
from users.models import Skill



class NotificationView(APIView):
    def get(self, request):
        user = request.user
        
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        
        serializer = NotificationSerializer(notifications, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "data": serializer.data,
        }
        return Response(response_data , status=status.HTTP_200_OK)
    

class SkillView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "data": serializer.data,
        }
        return Response(response_data , status=status.HTTP_200_OK)
    def post(self, request):
        data = request.data 
        # check this name is already exists 
        skill = Skill.objects.filter(name=data['name']).first()
        if skill:
            return Response({"message": "Skill already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SkillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FeedJobView(APIView):
    def get(self, request,pk=None, *args, **kwargs):
        user = request.user
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
            vacancy = Vacancy.objects.filter(job__company=client).select_related('job','job_title', 'uniform').prefetch_related('skills', 'participants').order_by('open_date', 'start_time')
            serializer = VacancySerializer(vacancy, many=True)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        if pk:
            vacancy = Vacancy.objects.filter(pk=pk).select_related('job','job_title','uniform').prefetch_related('skills','participants').first()
            serializer = VacancySerializer(vacancy)
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "data": serializer.data,
            }
            return Response(response)
        
        vacancy = Vacancy.objects.filter(job_status='active').select_related('job','job_title', 'uniform').prefetch_related('skills', 'participants').order_by('open_date', 'start_time')
        serializer = VacancySerializer(vacancy, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    

class GetJobTemplateAPIView(APIView):
    def get(self, request, pk=None):
        user = request.user 
        if user.is_client:
            client = user.profiles 
            if pk:
                job_template = JobTemplate.objects.filter(client=client, pk=pk).first()
                if job_template:
                    serializer = JobTemplateSserializers(job_template)
                    response_data = {
                        "status": status.HTTP_200_OK,
                        "success": True,
                        "data": serializer.data,
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Job template not found"}, status=status.HTTP_404_NOT_FOUND)
            job_template = JobTemplate.objects.filter(client=client)
            serializer = JobTemplateSserializers(job_template, many=True)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "data": serializer.data,
            }
            return Response(response_data , status=status.HTTP_200_OK)
            