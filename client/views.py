from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView




from .models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy,
    JobApplication,
    StaffInvitation

)
from .serializers import (
    CompanyProfileSerializer,
    JobTemplateSerializer,
    JobSerializer,
    VacancySerializer,
    CreateVacancySerializers,
    JobApplicationSerializer
)

from dashboard.models import Notification

# create company profile

class CompanyProfileCreateView(generics.ListCreateAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # create company profile with custom respones in post request
    def create(self, request, *args, **kwargs):
        serializer = CompanyProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response = {
                "status": status.HTTP_200_OK,
                "message": "Company profile created successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # update profile
    def put(self, request, pk):
        company_profile = CompanyProfile.objects.get(pk=pk)
        serializer = CompanyProfileSerializer(company_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "message": "Company profile updated successfully",
                "data": serializer.data
                
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VacancyView(APIView):
    def get(self, request, pk=None):
        if pk:
            vacancy = get_object_or_404(Vacancy, pk=pk)
            serializer = VacancySerializer(vacancy)
            return Response(serializer.data)
        
        vacancies = Vacancy.objects.all()
        serializer = VacancySerializer(vacancies, many=True)
        return Response(serializer.data)
    def post(self, request):
        data = request.data
        print('data', data)
        serializer = CreateVacancySerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # update vacancy 
    

class JobView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            job = get_object_or_404(Job, pk=pk)
            serializer = JobSerializer(job)
            return Response(serializer.data)
        
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = JobSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    # custom response 
    
    def update(self, request, pk):
        job = Job.objects.get(pk=pk)
        serializer = JobSerializer(job, data=request.data)
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
        

class JobApplicationAPI(APIView):
    def get(self, request,pk=None):
        if pk:
            job_application = get_object_or_404(JobApplication, pk=pk)
            serializer = JobApplicationSerializer(job_application)
            return Response(serializer.data)
        
        job_applications = JobApplication.objects.all()
        serializer = JobApplicationSerializer(job_applications, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        job_application = get_object_or_404(JobApplication, pk=pk)
        job_application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class InviteStaffView(APIView):
    def post(self, request, vacancy_id=None):
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        
class AcceptApplicantView(APIView):
    def post(self, request, application_id=None):
        application = get_object_or_404(JobApplication, pk=application_id)
        vacancy = application.vacancy
        application.status = True
        staff = application.applicant
        vacancy.participants.add(staff)
        # send notification to applicant 
        Notification.objects.create(
            user = staff.user,
            message = f"Your application for {vacancy.job_title} has been accepted",
            
        )
        application.save()
        return Response(status=status.HTTP_200_OK)