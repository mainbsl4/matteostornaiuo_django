from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics 
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .models import FavouriteStaff, CompanyReview, Notification
from . serializers import (
    FavouriteStaffSerializer, 
    CompanyReviewSerializer, 
    StaffReviewSerializer, 
    NotificationSerializer, 
    SkillSerializer
)

from client.models import CompanyProfile, Vacancy
from staff.models import Staff
from users.models import Skill


class FavouriteStaffView(APIView):
    def get(self, request,company_id=None,pk=None):
        if pk:
            favourite = FavouriteStaff.objects.filter(staff__id=pk).first()
            if favourite:
                serializer = FavouriteStaffSerializer(favourite)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            favourites = FavouriteStaff.objects.filter(company__id=company_id)
            serializer = FavouriteStaffSerializer(favourites, many=True)
            return Response(serializer.data)
        
    def post(self, request,company_id=None, pk=None):
        data = request.data
        company = CompanyProfile.objects.filter(id=company_id).first()
        staff = Staff.objects.filter(id=data['staff_id']).first()
        favourite_staff,_ = FavouriteStaff.objects.get_or_create(company=company)

        if not company or not staff:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if data['action'] == 'add':
            favourite_staff.staff.add(staff)
            return Response({"message": "Favourite staff added successfully"})
        elif data['action'] =='remove':
            if staff in favourite_staff.staff.all():
                favourite_staff.staff.remove(staff)

            return Response({"message": "Favourite staff removed successfully"})
        

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