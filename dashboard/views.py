from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics 
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .models import  CompanyReview, Notification
from . serializers import (

    CompanyReviewSerializer, 
    StaffReviewSerializer, 
    NotificationSerializer, 
    SkillSerializer
)

from client.models import CompanyProfile, Vacancy
from staff.models import Staff
from users.models import Skill




class CompanyReviewView(APIView):
    def get(self, request, vacancy_id=None, pk=None, *args, **kwargs):
        if pk:
            review = get_object_or_404(CompanyReview, pk=pk)
            serializer = CompanyReviewSerializer(review)
            return Response(serializer.data)
        
        reviews = CompanyReview.objects.filter(vacancy__id=vacancy_id)
        serializer = CompanyReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    def post(self, request, vacancy_id=None):
        user = request.user
        staff = Staff.objects.filter(user=user).first()
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        company = vacancy.vacancies.first().company
        serializer = CompanyReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(staff=staff, vacancy=vacancy, profile = company )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StaffReviewView(APIView):
    def get(self, request, vacancy_id=None, pk=None, *args, **kwargs):
        if pk:
            review = get_object_or_404(CompanyReview, pk=pk)
            serializer = StaffReviewSerializer(review)
            return Response(serializer.data)
        
        reviews = CompanyReview.objects.filter(vacancy__id=vacancy_id)
        serializer = StaffReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request, staff_id=None, *args, **kwargs):
        vacancy_id = request.data['vacancy_id']
        
        staff = Staff.objects.filter(id=staff_id).first()
        vacancy = Vacancy.objects.get(id=vacancy_id)
        company = vacancy.vacancies.first().company
        
        
        serializer = StaffReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(staff=staff,vacancy=vacancy, profile=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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