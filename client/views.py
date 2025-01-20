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
    StaffInvitation,
    Checkin,
    Checkout,


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

)

from dashboard.models import Notification
from staff.models import Staff

# create company profile

class CompanyProfileCreateView(generics.ListCreateAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer

    # format the response in get request
    
    def list(self, request, format=None):
        queryset = CompanyProfile.objects.filter(user=request.user).first()
        serializer = CompanyProfileSerializer(queryset)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of company profiles",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

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
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Vacancy details",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        vacancies = Vacancy.objects.all()
        serializer = VacancySerializer(vacancies, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of vacancies",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
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
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job details",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        jobs = Job.objects.all()
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    # custom response 
    def list(self, request):
        queryset = Job.objects.filter(user=request.user).first()
        serializer = JobSerializer(queryset)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of your jobs",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
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
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job application details",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        job_applications = JobApplication.objects.all()
        serializer = JobApplicationSerializer(job_applications, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job applications",
                "data": serializer.data
    
        }
        return Response(response_data, status=status.HTTP_200_OK)
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
    
class CheckInView(APIView):

    def get(self, request, vacancy_id=None, *args, **kwargs):
        checkins = Checkin.objects.filter(vacancy__id=vacancy_id)
        serializer = CheckinSerializer(checkins, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of checkins",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, vacancy_id=None):
        data = request.data
        user = request.user
        staff = Staff.objects.filter(user=user).first()
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        serializer = CheckinSerializer(data=data)
        if serializer.is_valid():
            serializer.save(staff=staff, vacancy=vacancy)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CheckOutView(APIView):
    def post(self, request, vacancy_id=None):
        data = request.data
        user = request.user
        staff = Staff.objects.filter(user=user).first()
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        serializer = CheckOutSerializer(data=data)
        if serializer.is_valid():
            serializer.save(staff=staff, vacancy=vacancy)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get(self, request,vacancy_id=None, pk=None, *args, **kwargs):
        if pk:
            checkout = get_object_or_404(Checkout, pk=pk)
            serializer = CheckOutSerializer(checkout)
            return Response(serializer.data)
        checkout = get_object_or_404(Checkout, vacancy__id=vacancy_id)
        serializer = CheckOutSerializer(checkout)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Check-out details",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
# approval check in checkout request

class ApproveCheckinView(APIView):

    # get request
    def get(self, request, vacancy_id=None, *args, **kwargs):
        checkins = Checkin.objects.filter(vacancy__id=vacancy_id) # add status = false
        serializer = CheckinSerializer(checkins, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of pending check-in requests",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    def post(self, request, vacancy_id=None, pk=None):
        staff_id = request.data['staff_id']
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        checkin = get_object_or_404(Checkin, vacancy=vacancy, staff__id=staff_id)
        checkin.status = True
        checkin.save()
        # send notification to staff
        notification = Notification.objects.create(
            user = checkin.staff.user,
            message = f"Your check-in request for {vacancy.job_title} has been approved",
            
        )
        return Response(status=status.HTTP_200_OK)
    
class ApproveCheckoutView(APIView):

    # get request
    def get(self, request, vacancy_id=None, *args, **kwargs):
        """ list of pending checkout list."""
        checkouts = Checkout.objects.filter(vacancy__id=vacancy_id) # add status = false
        serializer = CheckOutSerializer(checkouts, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of pending check-out requests",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    def post(self, request, vacancy_id=None, pk=None):
        staff_id = request.data['staff_id']
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        checkout = get_object_or_404(Checkout, vacancy=vacancy, staff__id=staff_id)

        checkout.status = True
        checkout.save()
        # send notification to staff
        notification = Notification.objects.create(
            user = checkout.staff.user,
            message = f"Your check-out request for {vacancy.job_title} has been approved",
            
        )
        return Response(status=status.HTTP_200_OK)
    

