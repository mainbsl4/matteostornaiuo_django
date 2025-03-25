import os
from datetime import datetime
from weasyprint import HTML


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q, Avg
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.html import strip_tags
from django.conf import settings

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy,
    JobApplication,
    StaffInvitation,
    Checkin,
    Checkout,
    JobAds,
    FavouriteStaff,
    MyStaff,
    JobReport,
    CompanyReview

)

from .serializers import (
    CompanyProfileSerializer,
    JobTemplateSerializer,
    JobSerializer,
    VacancySerializer,
    CreateVacancySerializers,
    JobApplicationSerializer,
    CheckinSerializer,
    CheckOutSerializer,
    PermanentJobsSerializer,
    FavouriteStaffSerializer,
    MyStaffSerializer,
    CompanyReviewSerializer

)

from dashboard.models import Notification
from staff.models import Staff
from staff.serializers import StaffSerializer
from shifting.models import DailyShift, Shifting
from shifting.serializers import DailyShiftSerializer
# create company profile

class CompanyProfileCreateView(generics.ListCreateAPIView):
    def list(self, request, format=None):
        try:
            user = request.user
            if user.is_client:
                queryset = CompanyProfile.objects.get(user=request.user)
            else:
                return Response({"error": "Only client can access this endpoint"}, status=status.HTTP_400_BAD_REQUEST)
        except CompanyProfile.DoesNotExist:
            return Response({"error": "Company profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CompanyProfileSerializer(queryset)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Company profiles",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # create company profile with custom respones in post request
    def create(self, request, *args, **kwargs):
        # if already have a company profile 
        if CompanyProfile.objects.filter(user=request.user).exists():
            return Response({"error": "You already have a company profile"}, status=status.HTTP_400_BAD_REQUEST)
        
        # if not, create a new one
        serializer = CompanyProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Company profile created successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # update profile
    def put(self, request):
        company_profile = CompanyProfile.objects.get(user=request.user)
        serializer = CompanyProfileSerializer(company_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Company profile updated successfully",
                "data": serializer.data
                
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid data",
                "data": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class VacancyView(APIView):
    def get(self, request,job_id=None, pk=None, **kwargs):
        if job_id:
            vacancy = Vacancy.objects.filter(job__id=job_id)
            serializer = VacancySerializer(vacancy, many=True)
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Vacancies",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        if pk:
            vacancy = get_object_or_404(Vacancy, pk=pk)
            serializer = VacancySerializer(vacancy)
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Vacancy details",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
        # return error response
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        
        serializer = CreateVacancySerializers(data=request.data)
        if serializer.is_valid():
            vacancy = serializer.save()
            response = VacancySerializer(vacancy)
            response_data = {
                "status": status.HTTP_200_OK,
                "message": "Vacancy created successfully",
                "data": response.data
                
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        user = request.user
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
        else:
            return Response({"error": "Only client can access this endpoint"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            vacancy = Vacancy.objects.get(pk=pk)
            if vacancy.job.company!= client:
                return Response({"error": "You are not authorized to access this vacancy"}, status=status.HTTP_403_FORBIDDEN)
        except Vacancy.DoesNotExist:
            return Response({"error": "Vacancy not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CreateVacancySerializers(instance=vacancy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = VacancySerializer(vacancy)
            response_data = {
                "status": status.HTTP_200_OK,
                "message": "Vacancy updated successfully",
                # "data": response.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
            if not client:
                return Response({"error": "Company profile not found"}, status=status.HTTP_404_NOT_FOUND)
            vacancy = Vacancy.objects.filter(pk=pk, job__company=client).first()
            if not vacancy:
                return Response({"error": "You are not authorized to delete this vacancy"}, status=status.HTTP_403_FORBIDDEN)
            vacancy.delete()
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Vacancy deleted successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)

class JobView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        user=request.user
        client = CompanyProfile.objects.filter(user=user).first()
        if pk:
            job = Job.objects.filter(company=client, pk=pk).first()
            if not job:
                return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = JobSerializer(job)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,  
                "message": "Job details",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        jobs = Job.objects.filter(company=client)
        serializer = JobSerializer(jobs, many=True)
        response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job details",
                "data": serializer.data
            }
        return Response(response_data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = JobSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job created successfully",
                # "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # update job
    def put(self, request, pk):
        job = Job.objects.get(pk=pk)
        serializer = JobSerializer(job, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "message": "Job updated successfully",
                "data": serializer.data
                
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = request.user
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
            if not client:
                return Response({"error": "Company profile not found"}, status=status.HTTP_404_NOT_FOUND)
            job = Job.objects.filter(pk=pk).first()
            if not job:
                return Response({"error": "You are not authorized to delete this job"}, status=status.HTTP_403_FORBIDDEN)
            if job.company == client:
                job.delete()
                response_data = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Job deleted successfully"
                }
                return Response(response_data, status=status.HTTP_200_OK)
            return Response({"error": "You are not authorized to delete this job"}, status=status.HTTP_403_FORBIDDEN)
        

class JobApplicationAPI(APIView): # pending actions page approve job
    def get(self, request, vacancy_id=None,pk=None):
        user = request.user
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
        else:
            return Response({"error": "Only clients can access this endpoint"}, status=status.HTTP_403_FORBIDDEN)
        # not used
        if pk:
            job_application = JobApplication.objects.filter(pk=pk, vacancy__client=client, is_approve = False).first()
            if not job_application:
                return Response({"error": "Job application not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = JobApplicationSerializer(job_application)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job application details",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        # use in job details application list
        if vacancy_id:
            try:
                vacancy = Vacancy.objects.get(id=vacancy_id)
            except Vacancy.DoesNotExist:
                return Response({"error": "Vacancy not found"}, status=status.HTTP_404_NOT_FOUND)
            job_applications = JobApplication.objects.filter(vacancy=vacancy, is_approve=False).select_related('vacancy','applicant').order_by('created_at')

            # serializer = JobApplicationSerializer(job_applications, many=True)
            applications = []
            for application in job_applications:
                obj = {
                    "id": application.id,
                    "staff_name": application.applicant.user.first_name + application.applicant.user.last_name,
                    "staff_profile": application.applicant.avatar.url if application.applicant.avatar else None,
                    "age": application.applicant.age,
                    "gender": application.applicant.gender,
                    "timesince": application.created_at,
                }
                applications.append(obj)

            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job applications",
                "data": applications
            }
            return Response(response_data, status=status.HTTP_200_OK)


        # use in pending action page
        vacancy_list = Vacancy.objects.filter(job__company=client, job_status__in=['active','pending', 'accepted']).only('id')

        job_applications = JobApplication.objects.filter(vacancy__in=vacancy_list).select_related('vacancy','applicant').order_by('created_at')
        # job_applications = JobApplication.objects.filter(vacancy__id=vacancy_id).order_by('-created_at')
        # serializer = JobApplicationSerializer(applications, many=True)
        applications = []
        for application in job_applications:
            obj = {
                "id": application.id,
                "staff_name": application.applicant.user.first_name + application.applicant.user.last_name,
                "staff_profile": application.applicant.avatar.url if application.applicant.avatar else None,
                "age": application.applicant.age,
                "gender": application.applicant.gender,
                "timesince": application.created_at,
            }
            applications.append(obj)
        response_data = {
            "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job applications",
                "data": applications
        }
        return Response(response_data, status=status.HTTP_200_OK)
    def post(self, request,vacancy_id=None,pk=None):
        data = request.data # id, status
        user = request.user 
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
            try:
                job_application = JobApplication.objects.get(id=pk)
            except JobApplication.DoesNotExist:
                return Response({"error": "Job application not found"}, status=status.HTTP_404_NOT_FOUND)
            
            if job_application.vacancy.job.company != client:
                return Response({"error": "Only client can approve this job application"}, status=status.HTTP_403_FORBIDDEN)
            
            # check expired job 
            if job_application.vacancy.close_date < datetime.now().date():
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "This job has expired"})
                
            # check already approved job
            if job_application.is_approve:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "This job application has already been approved"})

            # when accept job from job detail view
            # if vacancy_id:
            #     try:
            #         vacancy = Vacancy.objects.get(id=vacancy_id)
            #         application = JobApplication.objects.get(id=pk)
            #     except Vacancy.DoesNotExist:
            #         return Response({"error": "Vacancy/application not found"}, status=status.HTTP_404_NOT_FOUND)
            #     if vacancy.client!= client:
            #         return Response({"error": "Only client can approve the job request"}, status=status.HTTP_403_FORBIDDEN)
            #     if vacancy.participants.count() >= vacancy.number_of_staff:
            #         # no space response
            #         return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "No space for applicants"})
                
            #     if data['status'] == True:
            #         vacancy.participants.add(application.applicant)

            #         application.job_status = 'accepted'
            #         application.is_approve = True
            #         application.save()
            #         # send notification to staff
            #         Notification.objects.create(
            #             user = application.applicant.user,
            #             message = f"Your application for {application.vacancy.job_title} has been accepted",
            #         )
            #         return Response(status=status.HTTP_200_OK, data={"message": "Job application accepted"})
                    
            #     elif data['status'] == False:
            #         job_application.job_status ='rejected'
            #         job_application.is_approve = False
            #         job_application.save()
            #         # send notification to staff
            #         # Notification.objects.create(
            #         #     user = job_application.applicant.user,
            #         #     message = f"Your application for {job_application.vacancy.job_title} has been declined",
            #         # )
            #         return Response(status=status.HTTP_200_OK, data={"message": "Job application declined"})
            
            if data['status'] == True:
                vacancy = job_application.vacancy
                if vacancy.participants.count() >= vacancy.number_of_staff:
                    # no space response
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "No space for applicants"})
                
                # if not vacancy.participants.is_available:
                #     return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "You have another job schedule at that time!!"})
                # is staff have any entry on jobapplication on the same date and same time of this job
                if JobApplication.objects.filter(applicant=job_application.applicant, vacancy__open_date=job_application.vacancy.open_date, vacancy__start_time=job_application.vacancy.start_time, is_approve=False).exclude(id=job_application.id).exists():
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "You have another job schedule at that time!!"})


                vacancy.participants.add(job_application.applicant)
                
                job_application.job_status = 'accepted'
                job_application.is_approve = True
                job_application.save()

                full_name = job_application.applicant.user.first_name + ' ' + job_application.applicant.user.last_name
                time = f'{vacancy.open_date} at {vacancy.start_time}'
                html_content = render_to_string(
                    'contact.html', {
                    'staff_name': full_name,
                    'vacancy_name': vacancy.job_title.name,
                    'starting_date_time': time,
                    'price_per_hour': vacancy.job_title.staff_price,
                    'location': vacancy.location,
                    'company_name': vacancy.job.company,
                    'company_website': 'https://www.example.com',
                    'year': '2025',
                })

                # Convert HTML to PDF
                pdf_file = HTML(string=html_content).write_pdf()

                # Define storage path
                pdf_filename = f"job_contacts/job_contact_{job_application.id}.pdf"
                pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)

                # Save PDF in Django storage
                default_storage.save(pdf_filename, ContentFile(pdf_file))

                # Send email
                send_mail(
                    subject='Job Contact File',
                    message=strip_tags(html_content),  # Plain text version
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[job_application.applicant.user.email],
                    html_message=html_content,  # HTML version
                )

                # send notification to staff
                Notification.objects.create(
                    user = job_application.applicant.user,
                    message = f"Your application for {job_application.vacancy.job_title} has been approved",
                )
                return Response(status=status.HTTP_200_OK, data={"message": "Job application approved"})
            elif data['status'] == False:
                job_application.job_status = 'rejected'
                job_application.is_approve = False
                job_application.save()
                # send notification to staff
                # Notification.objects.create(
                #     user = job_application.applicant.user,
                #     message = f"Your application for {job_application.vacancy.job_title} has been declined",
                # )
                return Response(status=status.HTTP_200_OK, data={"message": "Job application declined"})
            
        
    # def delete(self, request, pk=None):
    #     job_application = get_object_or_404(JobApplication, pk=pk)
    #     job_application.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    

class CheckInView(APIView):

    def get(self, request, vacancy_id=None, pk=None, *args, **kwargs):
        user = request.user
        client = CompanyProfile.objects.get(user=user)

        if vacancy_id:
            try:
                vacancy = Vacancy.objects.get(id=vacancy_id)
            except Vacancy.DoesNotExist:
                return Response({"error": "Vacancy not found"}, status=status.HTTP_404_NOT_FOUND)
            applications = JobApplication.objects.select_related('vacancy', 'applicant').filter(vacancy=vacancy, is_approve=True, checkin_approve=False)
            serializer = JobApplicationSerializer(applications, many=True)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job checkin request",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

        vacancy = Vacancy.objects.filter(job__company=client, job_status__in=['active', 'progress', 'finished']).select_related('jo','uniform','job_title').prefetch_related('skills','participants')

        try:
            applications = JobApplication.objects.select_related('vacancy', 'applicant').filter(vacancy__in=vacancy,is_approve=True, checkin_approve=False)
        except JobApplication.DoesNotExist:
            return Response({"error": "No job checkin request found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = JobApplicationSerializer(applications, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Job Checkin Request",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

    
    def post(self, request, vacancy_id=None, pk=None, *args, **kwargs):
        user = request.user
        try:
            client = CompanyProfile.objects.get(user=user)
        except CompanyProfile.DoesNotExist:
            return Response({"error": "User is not a client"}, status=status.HTTP_403_FORBIDDEN)
        try:
            application = JobApplication.objects.get(id=pk)
        except JobApplication.DoesNotExist:
            return Response({"error": "Job application not found"}, status=status.HTTP_404_NOT_FOUND)
        if application.vacancy.job.company != client:
            return Response({"error": "Only client can check in this job application"}, status=status.HTTP_403_FORBIDDEN)
        if application.checkin_approve:
            return Response({"error": "Job check-in request has already been approved"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not application.is_approve:
            return Response({"error": "Job application has not been approved yet"}, status=status.HTTP_400_BAD_REQUEST)
        if not application.in_time or not application.checkin_location:
            return Response({"error": "Job application has not been checked in yet"}, status=status.HTTP_400_BAD_REQUEST)
        
        application.checkin_approve = True
        application.save()
        # send notification to staff
        Notification.objects.create(
            user = application.applicant.user,
            message = f"Your check-in request for {application.vacancy.job_title} has been approved",
        )
        return Response(status=status.HTTP_200_OK, data={"message": "Job check-in request approved"})
    

class CheckOutView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        user = request.user
        try:
            client = CompanyProfile.objects.get(user=user)
        except CompanyProfile.DoesNotExist:
            return Response({"error": "User is not a client"}, status=status.HTTP_403_FORBIDDEN)
        
        vacancy = Vacancy.objects.filter(job__company=client, job_status__in=['active', 'progress', 'finished']).select_related('jo','uniform','job_title').prefetch_related('skills','participants')

        job_application = JobApplication.objects.select_related('vacancy','applicant').filter(vacancy__in=vacancy,checkin_approve=True, job_status='accepted')
        
        serializer = JobApplicationSerializer(job_application, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of pending check-out requests",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, pk, **kwargs):
        user = request.user
        try:
            client = CompanyProfile.objects.get(user=user)
        except CompanyProfile.DoesNotExist:
            return Response({"error": "User is not a client"}, status=status.HTTP_403_FORBIDDEN)
        try:
            application = JobApplication.objects.get(id=pk)
            if application.vacancy.job.company != client:
                return Response({"error": "Only client can check out this job application"}, status=status.HTTP_403_FORBIDDEN)
        except JobApplication.DoesNotExist:
            return Response({"error": "Job application not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not application.checkin_approve:
            return Response({"error": "Job check-in request has not been approved yet"}, status=status.HTTP_400_BAD_REQUEST)
        
        if application.vacancy.job.company != client:
            return Response({"error": "Only client can check out this job application"}, status=status.HTTP_403_FORBIDDEN)
        
        if not application.out_time or not application.checkout_location:
            return Response({"error": "Job application has not been checked out yet"}, status=status.HTTP_400_BAD_REQUEST)
        
        if application.checkout_approve:
            return Response({"error": "Job check-out request has already been completed"}, status=status.HTTP_400_BAD_REQUEST)
                
        application.job_status = 'completed'
        application.checkout_approve = True
        # create report 
        report = JobReport.objects.create(
            job_application = application,
        )
        
        application.save()
        
        # send notification to staff
        Notification.objects.create(
            user = application.applicant.user,
            message = f"Your check-out request for {application.vacancy.job_title} has been completed",
        )
        return Response(status=status.HTTP_200_OK, data={"message": "Job check-out request completed"})
        

class JobAdsView(APIView):

    def get(self, request,pk=None,*args,**kwargs):
        user = request.user
        company = get_object_or_404(CompanyProfile, user=user)

        if pk:
            permanent_job = JobAds.objects.filter(company=company, id=pk).first()
            if not permanent_job:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "Permanent job not found"})
            serializer = PermanentJobsSerializer(permanent_job)
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Permanent job details",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
        permanent_jobs = JobAds.objects.filter(company=company)
        
        serializer = PermanentJobsSerializer(permanent_jobs, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of permanent jobs",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, **kwargs):
        data = request.data
        
        serializer = PermanentJobsSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Permanent job created successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid data",
                "data": serializer.errors
            }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        data = request.data
        user = request.user
        company = get_object_or_404(CompanyProfile, user=user)
        permanent_job = JobAds.objects.get(id=pk)
        if permanent_job.company == company:
            serializer = PermanentJobsSerializer(permanent_job, data=data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Permanent job updated successfully",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid data",
                "data": serializer.error
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
class ShiftCheckinAcceptView(APIView):
    def get(self, request, shifting_id=None, pk=None, *args, **kwargs):
        user = request.user
        company = get_object_or_404(CompanyProfile, user=user)
        shifting = Shifting.objects.get(id=shifting_id)
        if shifting.company == company:
            daily_shifts = DailyShift.objects.filter(shift=shifting)
            serializer = DailyShiftSerializer(daily_shifts, many=True)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "List of daily shifts",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        response = {
            "status": status.HTTP_403_FORBIDDEN,
            "success": False,
            "message": "You are not authorized to view this shifting"
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request, shifting_id=None, pk=None):
        user = request.user
        data = request.data
        company = get_object_or_404(CompanyProfile, user=user)
        shifting = Shifting.objects.get(id=shifting_id)
        if shifting.company == company:
            daily_shift = DailyShift.objects.get(id=pk)
            if data['type'] == 'checkin':
                daily_shift.checkin_status = True
                daily_shift.checkin_time = timezone.now()
                daily_shift.save()
                notification = Notification.objects.create(
                user = daily_shift.staff.user,
                message = f"Your check-in request for  has been approved", # need to add the 
                
                )
                response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Check-in status updated successfully"
                }
            elif data['type'] == 'checkout':
                daily_shift.checkout_status = True
                daily_shift.checkout_time = timezone.now()
                daily_shift.save()
                notification = Notification.objects.create(
                user = daily_shift.staff.user,
                message = f"Your check-out request for  has been approved", 
                )
                response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Check-out status updated successfully"
                }
            # send notification
            
            
            return Response(response_data, status=status.HTTP_200_OK)

class FavouriteStaffView(APIView):
    def get(self, request):
        user = request.user
        company = get_object_or_404(CompanyProfile, user=user)

        favourites = FavouriteStaff.objects.filter(company = company)
        if not favourites:
            response = {
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Favourite staff not found",
                "data"   : []
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        
        # serializer = FavouriteStaffSerializer(favourites, many=True, fields=['staff'])
        staff_list = []
        for staff in favourites:
            data = {
                "id": staff.staff.id,
                "first_name": staff.staff.user.first_name,
                "last_name": staff.staff.user.last_name,
                "avatar": staff.staff.avatar.url if staff.staff.avatar else None,
                "role": staff.staff.role.name,
                # "experience": staff.staff.experience.all(),
                "age": staff.staff.age,
            }
            staff_list.append(data)

        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of favourite staff",
            "data": staff_list
        }
        return Response(response,status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        user = request.user
        if not user.is_client:
            response = {
                "status": status.HTTP_403_FORBIDDEN,
                "success": False,
                "message": "Only clients can add favourite staff"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        
        company = get_object_or_404(CompanyProfile, user=user)

        try:
            staff = Staff.objects.select_related('user','role').prefetch_related('skills','experience').get(id=pk)
        except Staff.DoesNotExist:
            response = {
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Staff Profile not found"
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        
        favourite_staff = FavouriteStaff.objects.filter(company=company, staff=staff).first() 

        # if already added then remove it 
        if favourite_staff:
            favourite_staff.delete()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Staff removed from favourite staff list successfully"
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            favourite_staff = FavouriteStaff.objects.create(company=company, staff=staff)
            response = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Staff added to favourites successfully"
            }
            return Response(response, status=status.HTTP_201_CREATED)
    

class MyStaffView(APIView):
    def get(self, request, pk=None):
        user = request.user
        company = get_object_or_404(CompanyProfile, user=user)
        mystaff = MyStaff.objects.filter(client=company, status = True)
        serializer = MyStaffSerializer(mystaff, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of staff",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)



class CompanyReviewView(APIView):
    def get(self, request):
        user = request.user
        if user.is_client:
            client = get_object_or_404(CompanyProfile, user=user)
            reviews = CompanyReview.objects.filter(review_for=client)
            # calculate avg rating 
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            serializer = CompanyReviewSerializer(reviews, many=True)

            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Client's reviews",
                "data": [serializer.data,avg_rating]
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": status.HTTP_403_FORBIDDEN,
            "success": False,
            "message": "You are not authorized to view this client's reviews"
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, application_id):
        try:
            application = JobApplication.objects.get(id=application_id)
        except JobApplication.DoesNotExist:
            response = {
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Job application not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        if application.applicant.user == request.user:
            data = request.data 
            # if already reviewed 
            if CompanyReview.objects.filter(review_by = application.applicant, application=application).exists():
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "message": "You have already reviewed this client"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            review = CompanyReview.objects.create(
                review_by = application.applicant,
                review_for = application.vacancy.job.company,
                application=application,
                rating = data['rating'],
                content = data['content']
            )
            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Review submitted successfully",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response = {
            "status": status.HTTP_403_FORBIDDEN,
            "success": False,
            "message": "You are not authorized to review this client"
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    

class TipView(APIView):
    def post(self,request, report_id):
        user = request.user
        data = request.data
        report = get_object_or_404(JobReport, id=report_id)
        if report.job_application.vacancy.job.company.user == user:
            data = request.data
            report.tips += data['tips']
            report.save()

            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Tip added to staff working report sheet successfully"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response = {
            "status": status.HTTP_403_FORBIDDEN,
            "success": False,
            "message": "You are not authorized to submit a tip for this report"
        }
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    