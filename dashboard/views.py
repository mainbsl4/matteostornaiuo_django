from django.shortcuts import render, get_object_or_404
from datetime import date 
from datetime import datetime 
from django.db.models import Q , Count , Prefetch

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
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            user = request.user

            vacancy = Vacancy.objects.filter(pk=pk).select_related('job', 'job_title', 'uniform').prefetch_related('skills', 'participants').first()
                
            if not vacancy:
                return Response({"error": "Vacancy not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if vacancy.job.company.user == user:
                serializer = VacancySerializer(vacancy)
                response = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "data": serializer.data,
                }
                return Response(response)
            
        
        user = request.user
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
            if not client:
                return Response({"error": "Client profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
            job_status = request.query_params.get('status', None)
            open_date = request.query_params.get('date', None)
            time = request.query_params.get('time', None)
            search = request.query_params.get('search', None)
            location = request.query_params.get('location', None)
            
            vacancies = Vacancy.objects.filter(job__company=client).select_related(
                'job', 'job_title', 'uniform'
            ).prefetch_related(
                'skills', 'participants'
            ).order_by('-created_at')

            if search:
                vacancies = vacancies.filter(
                    Q(job__title__icontains=search) |
                    Q(skills__name__icontains=search) |
                    Q(job_title__name__icontains=search)
                ).distinct()

            if job_status:
                vacancies = vacancies.filter(job_status=job_status)

            if location:
                vacancies = vacancies.filter(location=location).order_by('-created_at')

            if open_date:
                try:
                    open_date = datetime.strptime(open_date, '%Y-%m-%d').date()
                    vacancies = vacancies.filter(Q(open_date=open_date) | Q(close_date=open_date)).order_by('-created_at')
                except ValueError:
                    return Response(
                        {"error": "Invalid open_date format, expected YYYY-MM-DD."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            if time:
                try:
                    time = datetime.strptime(time, '%H:%M:%S').time()
                    vacancies = vacancies.filter(Q(start_time=time) | Q(close_time=time)).order_by('-created_at')
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
            
            # Prefetch related JobApplications and annotate counts
            vacancies = vacancies.prefetch_related(
                Prefetch('jobapplication_set', queryset=JobApplication.objects.only('applicant__avatar'))
            ).annotate(
                pending_applications=Count('jobapplication', filter=Q(jobapplication__job_status='pending')),
                accepted_applications=Count('jobapplication', filter=Q(jobapplication__job_status='accepted')),
                rejected_applications=Count('jobapplication', filter=Q(jobapplication__job_status='rejected')),
                expired_applications=Count('jobapplication', filter=Q(jobapplication__job_status='expired'))
            ).order_by('-created_at')

            paginator = PageNumberPagination()
            paginator.page_size = 5
            paginated_vacancies = paginator.paginate_queryset(vacancies, request)
            
            job_list = []
            for vacancy in paginated_vacancies:
                data = {
                    "id": vacancy.id,
                    "job_status": vacancy.job_status,
                    "job_title": vacancy.job.title,
                    "job_id": vacancy.job.id,
                    "job_role_id": vacancy.job_title.id,
                    "uniform_id": vacancy.uniform.id if vacancy.uniform else None,
                    "skill_ids": [skl.id for skl in vacancy.skills.all()],
                    "company_logo": vacancy.job.company.company_logo.url if vacancy.job.company.company_logo else None,
                    "number_of_staff": vacancy.number_of_staff,
                    "start_date": vacancy.open_date,
                    "start_time": vacancy.start_time,
                    "end_time": vacancy.end_time,
                    "location": vacancy.location,
                    "applicant": [
                        app.applicant.avatar.url if app.applicant.avatar else app.applicant.user.first_name for app in vacancy.jobapplication_set.all()
                    ],
                    "application_status": {
                        "pending": vacancy.pending_applications,
                        "accepted": vacancy.accepted_applications,
                        "rejected": vacancy.rejected_applications,
                        "expired": vacancy.expired_applications
                    },
                }
                job_list.append(data)

            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "total_objects": paginator.page.paginator.count,
                "total_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "data": job_list,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        vacancies = Vacancy.objects.filter(job_status='active').select_related('job', 'job_title', 'uniform').prefetch_related('skills', 'participants').order_by('-created_at')
        serializer = VacancySerializer(vacancies, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class JobCountAPI(APIView):
    def get(self, request):
        user = request.user
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
            if not client:
                return Response({"error": "Client profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
            vacancies = Vacancy.objects.filter(job__company=client).select_related('job', 'job_title', 'uniform').prefetch_related('skills', 'participants')
            status_count = {
                "active": vacancies.filter(job_status='active').count(),
                "progress": vacancies.filter(job_status='progress').count(),
                "draft": vacancies.filter(job_status='draft').count(),
                "cancelled": vacancies.filter(job_status='cancelled').count(),
                "finished": vacancies.filter(job_status='finished').count(),
            }
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "data": status_count,
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
                    "description": template.job.description
                }
                template_list.append(data)

            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "data": template_list,
            }
            return Response(response_data , status=status.HTTP_200_OK)
        return Response({"message": "You are not authorized to access this resource"}, status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, pk):
        user = request.user 
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
            job_template = JobTemplate.objects.filter(client=client, id=pk).first()
            if not job_template:
                return Response({"message": "Job template not found"}, status=status.HTTP_404_NOT_FOUND)
            job_template.delete()
            return Response({"message": "Job template deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You are not authorized to access this resource"}, status=status.HTTP_403_FORBIDDEN)