from django.shortcuts import render, get_object_or_404
from datetime import date 
from datetime import datetime 
from django.db.models import Q 

from rest_framework import status, generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# Create your views here.
from .models import  Notification
from . serializers import (
    NotificationSerializer, 
    SkillSerializer,

)

from client.models import CompanyProfile, Vacancy, Job, JobTemplate, JobApplication
from client.serializers import VacancySerializer, JobTemplateSserializers, JobApplicationSerializer
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
            
            job_status = request.query_params.get('status', None)
            open_date = request.query_params.get('date', None)
            time = request.query_params.get('time', None)
            search = request.query_params.get('search', None)
            location = request.query_params.get('location', None)
            
            # Start with the base queryset
            vacancies = Vacancy.objects.filter(job__company=client).select_related(
                'job', 'job_title', 'uniform'
            ).prefetch_related(
                'skills', 'participants'
            ).order_by('open_date', 'start_time')

            if search:
                vacancies = vacancies.filter(
                    Q(job__title__icontains=search) |  # Search job title
                    # Q(location__icontains=search) |
                    Q(skills__name__icontains=search) |
                    Q(job_title__name__icontains=search)  # Search job location
                ).distinct()

            # Filter by job_status if provided
            if job_status:
                try:
                    vacancies = vacancies.filter(job_status=job_status)
                except ValueError:
                    return Response(
                        {"error": "Invalid job_status format."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            if location:
                try:
                    vacancies = vacancies.filter(location=location)
                except ValueError:
                    return Response(
                        {"error": "Invalid location format."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            # Filter by open_date if provided
            if open_date:
                try:
                    # Assuming open_date is in 'YYYY-MM-DD' format
                    open_date = datetime.strptime(open_date, '%Y-%m-%d').date()
                    vacancies = vacancies.filter(Q(open_date=open_date) | Q(close_date=open_date))
                except ValueError:
                    return Response(
                        {"error": "Invalid open_date format, expected YYYY-MM-DD."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            if time:
                try:
                    # Assuming time is in 'HH:MM' format
                    time = datetime.strptime(time, '%H:%M:%S').time()
                    vacancies = vacancies.filter(Q(start_time=time) | Q(close_time=time))
                except ValueError:
                    return Response(
                        {"error": "Invalid time format, expected HH:MM."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            if not vacancies.exists():
                return Response(
                    {"error": "No vacancies found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Pagination
            paginator = PageNumberPagination()
            paginator.page_size= 5
            vacancies = paginator.paginate_queryset(vacancies,request) 
            job_list = []
            def get_application_status(obj):
                # return the count of each job status 
                job_application = JobApplication.objects.filter(vacancy=obj)
                pending = job_application.filter(job_status='pending').count()
                accepted = job_application.filter(job_status='accepted').count()
                rejected = job_application.filter(job_status='rejected').count()
                expierd = job_application.filter(job_status='expired').count()
                return {'pending': pending, 'accepted': accepted,'rejected': rejected, 'expired': expierd}
        

            for vacancy in vacancies:
                applications = JobApplication.objects.filter(vacancy=vacancy).only('applicant__avatar')
                
                data = {
                    "id": vacancy.id,
                    "job_status": vacancy.job_status,
                    "job_title": vacancy.job.title,
                    "company_logo": vacancy.job.company.company_logo.url if vacancy.job.company.company_logo else None,
                    "number_of_staff": vacancy.number_of_staff,
                    "start_date": vacancy.open_date,
                    "start_time": vacancy.start_time,
                    "applicant": [
                        staff.applicant.avatar.url if staff.applicant.avatar else None for staff in applications
                        
                    ],
                    "application_status": get_application_status(vacancy),
                }
                job_list.append(data)

            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "total_objects": paginator.page.paginator.count,  # Total vacancies
                "total_pages": paginator.page.paginator.num_pages,  # Total pages
                "current_page": paginator.page.number,
                "data": job_list,
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
            client = CompanyProfile.objects.filter(user=user).first()
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
            templates = JobTemplate.objects.filter(client=client)
            # serializer = JobTemplateSserializers(job_template, many=True)
            if not templates.exists():
                return Response({"message": "No job template found"}, status=status.HTTP_404_NOT_FOUND)
            
            template_list = []
            for template in templates:
                data = {
                    "id": template.id,
                    "name": template.name,
                }
                template_list.append(data)

            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "data": template_list,
            }
            return Response(response_data , status=status.HTTP_200_OK)
        return Response({"message": "You are not authorized to access this resource"}, status=status.HTTP_403_FORBIDDEN)
            