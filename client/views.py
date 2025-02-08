from django.shortcuts import render, get_object_or_404
from django.utils import timezone

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
    MyStaff


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
    MyStaffSerializer

)

from dashboard.models import Notification
from staff.models import Staff
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
    def put(self, request, pk):
        company_profile = CompanyProfile.objects.get(pk=pk, user=request.user)
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
    def get(self, request, pk=None):
        user = request.user 
        client = CompanyProfile.objects.filter(user=user).first()

        if pk:
            vacancy = Vacancy.objects.filter(client=client, pk=pk).first()
            if not vacancy:
                return Response({"error": "Vacancy not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = VacancySerializer(vacancy)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Vacancy details",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        vacancies = Vacancy.objects.filter(client=client)
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
        serializer = CreateVacancySerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            vacancy = serializer.save()
            response = VacancySerializer(vacancy)
            response_data = {
                "status": status.HTTP_200_OK,
                "message": "Vacancy created successfully",
                # show response data in vacancy serializer
                "data": response.data
                
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # update vacancy 
    def put(self, request, pk):
        vacancy = Vacancy.objects.get(pk=pk)
        serializer = CreateVacancySerializers(vacancy, data=request.data, context={'request': request})
        if serializer.is_valid():
            res = serializer.save()
            response = VacancySerializer(res)
            response = {
                "status": status.HTTP_200_OK,
                "message": "Vacancy updated successfully",
                "data": response.data
                
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        job = get_object_or_404(Vacancy, pk=pk)
        job.delete()
        response = {
            "status": status.HTTP_204_NO_CONTENT,
            "success": True,
            "message": "Vacancy deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    
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
                "data": serializer.data
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
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        job.delete()
        response = {
            "status": status.HTTP_204_NO_CONTENT,
            "success": True,
            "message": "Job deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    

class JobApplicationAPI(APIView):
    def get(self, request, vacancy_id=None,pk=None):
        user = request.user
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
        else:
            return Response({"error": "Only clients can access this endpoint"}, status=status.HTTP_403_FORBIDDEN)
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
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return Response({"error": "Vacancy not found"}, status=status.HTTP_404_NOT_FOUND)
        job_applications = JobApplication.objects.filter(vacancy=vacancy).order_by('-created_at')
        # job_applications = JobApplication.objects.filter(vacancy__id=vacancy_id).order_by('-created_at')
        serializer = JobApplicationSerializer(job_applications, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job applications",
                "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    def post(self, request,vacancy_id,pk):
        data = request.data
        user = request.user 
        if user.is_client:
            client = CompanyProfile.objects.filter(user=user).first()
            vacancy = Vacancy.objects.filter(id=vacancy_id, client=client).first()
            
        staff = Staff.objects.filter(id=data['staff_id']).first()
        # vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        try:
            job_application = JobApplication.objects.get(id=pk)
            if job_application.vacancy.one_day_job:
                pass # do it later  
            if job_application.vacancy.participants == job_application.vacancy.number_of_staff:
                return Response({"error": "All participants have already applied for this vacancy"}, status=status.HTTP_400_BAD_REQUEST)
            elif staff in job_application.vacancy.participants.all():
                return Response({"error": "You have already applied for this vacancy"}, status=status.HTTP_400_BAD_REQUEST)
            if data['status'] == True:
                job_application.vacancy.participants.add(staff)
                job_application.is_approve = True 
                job_application.job_status = 'UPCOMMING'
                job_application.save()
                # send notification to staff
                Notification.objects.create(
                    user = staff.user,
                    message = f"You have been assigned to {vacancy.job_title} on {vacancy.open_date} in {vacancy.location} at {vacancy.start_time}",
                )
                return Response(status=status.HTTP_200_OK, data={"message": "Job application approved"})
            else:
                job_application.job_status = 'REJECTED'
                job_application.save()
                return Response(status=status.HTTP_200_OK, data={"message": "Job application rejected"})
            
        except Vacancy.DoesNotExist:
            return Response({"error": "Vacancy not found"}, status=status.HTTP_404_NOT_FOUND)
        except JobApplication.DoesNotExist:
            return Response({"error": "Job Application not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        
    
    def delete(self, request, pk=None):
        job_application = get_object_or_404(JobApplication, pk=pk)
        job_application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AcceptApplicantView(APIView):
    def post(self, request, application_id=None):
        application = get_object_or_404(JobApplication, pk=application_id)
        vacancy = application.vacancy
        if vacancy.one_day_job:
            daily_shift = DailyShift.objects.filter(
                day=vacancy.open_date, 
                start_time=vacancy.start_time, 
                end_time=vacancy.end_time,
                one_day_job = True
                ).first()
            if not daily_shift:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "No available daily shift"})
            daily_shift.staff = application.applicant
            daily_shift.status = True
            daily_shift.save()
            # send notification to staff
            Notification.objects.create(
                user = staff.user,
                message = f"You have been assigned to {vacancy.job_title} on {vacancy.open_date}",
                
            )


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
    def get(self, request,pk=None):
        user = request.user
        company = get_object_or_404(CompanyProfile, user=user)

        if pk:
            favourite = FavouriteStaff.objects.filter(company=company,pk=pk).first()
            if favourite:
                serializer = FavouriteStaffSerializer(favourite)
                response = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Favourite staff details",
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Favourite staff not found"
                }
                return Response(response,status=status.HTTP_404_NOT_FOUND)
        
        favourites = FavouriteStaff.objects.filter(company = company)
        serializer = FavouriteStaffSerializer(favourites, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "List of favourite staff",
            "data": serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
    def post(self, request, pk=None):
        user = request.user
        company = get_object_or_404(CompanyProfile, user=user)
        favourite_staff,_ = FavouriteStaff.objects.get_or_create(company=company)
        data = request.data        
        try:
            staff = Staff.objects.get(id=pk)
        except Staff.DoesNotExist:
            response = {
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Staff not found"
            }
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        
        if data['action'] == 'add':
            # check is staff already added
            if staff in favourite_staff.staff.all():
                return Response({"message": "Staff is already a favourite"})
            favourite_staff.staff.add(staff)
            return Response({"message": "Favourite staff added successfully"})
        elif data['action'] =='remove':
            if staff in favourite_staff.staff.all():
                favourite_staff.staff.remove(staff)
                return Response({"message": "Favourite staff removed successfully"})
            return Response({"message": "Staff is not a favourite"})

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
    

