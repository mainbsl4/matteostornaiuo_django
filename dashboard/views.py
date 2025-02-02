from django.shortcuts import render, get_object_or_404
from datetime import date 
from operator import itemgetter

from rest_framework import status, generics 
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .models import  CompanyReview, Notification
from . serializers import (

    CompanyReviewSerializer, 
    StaffReviewSerializer, 
    NotificationSerializer, 
    SkillSerializer,
    VacancyJobSerializer
)

from client.models import CompanyProfile, Vacancy, Job
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
    

class FeedJobView(APIView):
    def get(self, request):
        user = request.user
        today = date.today()

        # Check if the user is a staff member
        if user.is_staff:
            try:
                staff = Staff.objects.get(user=user)
                skills = set(staff.skills.all())  # Convert to set for faster intersection
                job_roles = set(staff.role.all())  # Convert to set for faster lookup

                # Fetch all published jobs with their vacancies
                jobs = Job.objects.filter(status='PUBLISHED').prefetch_related('vacancy')

                # Prepare a list to hold job-vacancy pairs with similarity scores
                feed_job = []

                for job in jobs:
                    for vacancy in job.vacancy.all():
                        # Initialize similarity score
                        similarity_score = 0

                        # Check if the vacancy is open today
                        if vacancy.open_date and vacancy.close_date:
                            if vacancy.open_date <= today <= vacancy.close_date:
                                similarity_score += 5  # Higher weight for today's jobs

                        # Add score for role match
                        if vacancy.job_title in job_roles:
                            similarity_score += 3  # Moderate weight for role match

                        # Add score for skill match
                        matching_skills = len(set(vacancy.skills.all()) & skills)  # Intersection of skills
                        similarity_score += matching_skills  # Weight for each matching skill

                        # Append job-vacancy pair with similarity score
                        feed_job.append({
                            "job": job,
                            "vacancy": vacancy,
                            "similarity_score": similarity_score
                        })

                # Sort jobs by similarity score (descending)
                feed_job.sort(key=itemgetter('similarity_score'), reverse=True)

                # Serialize the sorted data
                serializer = VacancyJobSerializer(
                    [{"job": item["job"], "vacancy": item["vacancy"]} for item in feed_job],
                    many=True
                ).data

                response = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "data": serializer,
                }
                return Response(response, status=status.HTTP_200_OK)

            except Staff.DoesNotExist:
                return Response(
                    {"status": status.HTTP_404_NOT_FOUND, "success": False, "message": "Staff profile not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If the user is not a staff member, return all jobs without sorting
        jobs = Job.objects.filter(status='PUBLISHED').prefetch_related('vacancy')
        feed_job = []
        for job in jobs:
            for vacancy in job.vacancy.all():
                feed_job.append({"job": job, "vacancy": vacancy})

        serializer = VacancyJobSerializer(feed_job, many=True).data
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "data": serializer,
        }
        return Response(response, status=status.HTTP_200_OK)
