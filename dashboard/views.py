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

)

from client.models import CompanyProfile, Vacancy, Job, JobTemplate
from client.serializers import VacancySerializer, JobTemplateSserializers
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
    def get(self, request, pk=None):
        user = request.user
        today = date.today()

        # If a specific vacancy ID (pk) is provided, return the details of that vacancy
        if pk:
            try:
                # Fetch the vacancy by its primary key with prefetching
                vacancy = Vacancy.objects.prefetch_related('skills', 'jobs').get(pk=pk)
                
                # Ensure the vacancy is connected to at least one job
                if not vacancy.jobs.exists():
                    return Response(
                        {"status": status.HTTP_404_NOT_FOUND, "success": False, "message": "Vacancy not connected to any job."},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Serialize the vacancy details
                serializer = VacancySerializer(vacancy)
                response = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "List of available jobs",
                    "data": serializer.data,
                }
                return Response(response, status=status.HTTP_200_OK)

            except Vacancy.DoesNotExist:
                return Response(
                    {"status": status.HTTP_404_NOT_FOUND, "success": False, "message": "Vacancy not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If no pk is provided, return the list of vacancies
        if user.is_staff:
            try:
                # Fetch the staff profile and their skills/roles
                staff = Staff.objects.get(user=user)
                skills = set(staff.skills.values_list('id', flat=True))  # Prefetch staff skills as IDs

                # Fetch all vacancies that are connected to at least one job
                vacancies = Vacancy.objects.filter(jobs__isnull=False).distinct().prefetch_related(
                    'skills', 'jobs'  # Prefetch related skills and jobs
                )

                # Annotate similarity scores for each vacancy
                feed_vacancies = []
                for vacancy in vacancies:
                    # Initialize similarity score
                    similarity_score = 0

                    # Add score for today's vacancies
                    if vacancy.open_date and vacancy.close_date:
                        if vacancy.open_date <= today <= vacancy.close_date:
                            similarity_score += 5  # Higher weight for today's vacancies

                    # Add score for skill match
                    matching_skills = len(set(v.id for v in vacancy.skills.all()) & skills)  # Intersection of skills
                    similarity_score += matching_skills  # Weight for each matching skill

                    # Append vacancy with similarity score
                    feed_vacancies.append({
                        "vacancy": vacancy,
                        "similarity_score": similarity_score
                    })

                # Sort vacancies by similarity score (descending)
                feed_vacancies.sort(key=lambda x: x['similarity_score'], reverse=True)

                # Serialize the sorted data
                serializer = VacancySerializer(
                    [item["vacancy"] for item in feed_vacancies],
                    many=True
                ).data

                response = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "List of available jobs",
                    "data": serializer,
                }
                return Response(response, status=status.HTTP_200_OK)

            except Staff.DoesNotExist:
                return Response(
                    {"status": status.HTTP_404_NOT_FOUND, "success": False, "message": "Staff profile not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If the user is not a staff member, return all vacancies connected to jobs
        vacancies = Vacancy.objects.all().exclude(job_status__in = ['cancelled', 'finished', 'draft']).distinct().prefetch_related('skills', 'jobs')

        # Serialize the data
        serializer = VacancySerializer(vacancies, many=True).data
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of available jobs",
            "data": serializer,
        }
        return Response(response, status=status.HTTP_200_OK)
    

class GetJobTemplateAPIView(APIView):
    def get(self, request, pk=None):
        user = request.user 
        if user.is_client:
            client = user.profiles 
            job_template = JobTemplate.objects.filter(client=client)
            serializer = JobTemplateSserializers(job_template, many=True)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "data": serializer.data,
            }
            return Response(response_data , status=status.HTTP_200_OK)
            