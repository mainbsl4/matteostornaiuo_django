from django.shortcuts import render
from django.utils import timezone
from datetime import datetime


from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Staff,
    Experience,
    BankDetails,

)
from .serializers import (
    StaffSerializer,
    CreateStaffSerializer,
    BankAccountSerializer,
    ExperienceSerializer,


)
from shifting.models import Shifting, DailyShift
from shifting.serializers import ShiftingSerializer, DailyShiftSerializer
from dashboard.models import Notification

from client.models import Job, JobApplication, Vacancy, MyStaff, Checkin, Checkout, JobRole
from client.serializers import JobApplicationSerializer, CheckinSerializer, CheckOutSerializer

from shifting.models import Shifting, DailyShift
from shifting.serializers import ShiftingSerializer, DailyShiftSerializer

class StaffProfileView(APIView):
    def get(self, request,pk=None, *args, **kwargs):
        user = request.user
        try:
            staff = Staff.objects.get(user=user)
        except Staff.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Staff profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if pk:
            try:
                staff = Staff.objects.get(id=pk)
            except Staff.DoesNotExist:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Staff not found"
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = StaffSerializer(staff)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Staff profile retrieved successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        serializer = StaffSerializer(staff)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Staff profile retrieved successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        serializer = CreateStaffSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            staff = serializer.save()
            # show staff serializers in response
            res = StaffSerializer(staff)
            response = {
                "status": status.HTTP_201_CREATED,
                "message": "Staff profile created successfully",
                "data": res.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        data = request.data
        user = request.user
        staff = Staff.objects.filter(user=user).first()
        if staff:
            serializer = CreateStaffSerializer(staff, data=data, partial=True)
            if serializer.is_valid():
                data = serializer.save()
                res = StaffSerializer(data)
                response = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Staff profile updated successfully",
                    "data": res.data
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "status": status.HTTP_404_NOT_FOUND,
            "message": "Staff profile not found"
        }, status=status.HTTP_404_NOT_FOUND)
    
class JobApplicationView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        user = request.user
        if not user.is_staff:
            return Response ({
                "status": status.HTTP_403_FORBIDDEN,
                "message": "Only staff can access this endpoint"
            })
        try:
            staff = Staff.objects.filter(user=user).first()
        except Staff.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Staff not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        applications = JobApplication.objects.filter(applicant=staff)
        if not applications:
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "No job applications found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        serializer = JobApplicationSerializer(applications, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Job applications retrieved successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request,pk=None, *args, **kwargs):
        user = request.user 
        if user.is_staff:
            staff = Staff.objects.filter(user=user).first()
            # check vacancy exists  and not expired or closed
            try:
                vacancy = Vacancy.objects.get(id=pk)
                if JobApplication.objects.filter(applicant=staff, vacancy=vacancy).exists():
                    response_data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "success": False,
                        "message": "You have already submitted a job application for this vacancy"
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                
                # check if application expired
                if vacancy.close_date < timezone.now().date():
                    response_data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "success": False,
                        "message": "This vacancy has expired"
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                
                # # check if vacancy is closed
                # if vacancy.is_closed:
                #     response_data = {
                #         "status": status.HTTP_400_BAD_REQUEST,
                #         "success": False,
                #         "message": "This vacancy is closed"
                #     }
                #     return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                
                # check if vacancy is already filled
                # if vacancy.is_full:
                #     response_data = {
                #         "status": status.HTTP_400_BAD_REQUEST,
                #         "success": False,
                #         "message": "This vacancy is already filled"
                #     }
                #     return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            except Vacancy.DoesNotExist:
                response_data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "message": "Vacancy Not Found"
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            application = JobApplication.objects.create(
                applicant = staff,
                vacancy=vacancy
            )
            # send notification to client
            notification = Notification.objects.create(
                user=vacancy.job.company.user,
                message=f'{staff} has submitted a job application for {vacancy.job_title}'
            )
            
            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Job application created successfully",
                "data": JobApplicationSerializer(application).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        # user must be a staff instance
        response_data = {
            "status": status.HTTP_403_FORBIDDEN,
            "success": False,
            "message": "You are not authorized to create this resource"
        }
        return Response(response_data, status=status.HTTP_403_FORBIDDEN)
    

class JobCheckinView(APIView): # jobapplication 
    def get(self, request, pk=None, *args, **kwargs):
        user = request.user
        try:
            staff = Staff.objects.get(user=user)
        except Staff.DoesNotExist:
            response_data = {
                "status": status.HTTP_403_FORBIDDEN,
                "success": False,
                "message": "You are not authorized to view this resource"
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        if pk:
            try:
                job_application = JobApplication.objects.get(applicant=staff, id=pk)
            except JobApplication.DoesNotExist:
                response_data = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Job not found"
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            serializer = JobApplicationSerializer(job_application)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Job retrieved successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        job_application = JobApplication.objects.filter(applicant=staff,is_approve=True)
        application_serializer = JobApplicationSerializer(job_application, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Job applications retrieved successfully",
            "data": application_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    def post(self, request,pk, *args, **kwargs):
        user = request.user
        data = request.data
        if user.is_staff:
            try:
                staff = Staff.objects.get(user=user)
            except Staff.DoesNotExist:
                response_data = {
                    "status": status.HTTP_403_FORBIDDEN,
                    "success": False,
                    "message": "You are not authorized to create this resource"
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)
            try:
                application = JobApplication.objects.get(id=pk, applicant=staff)
            except JobApplication.DoesNotExist:
                response_data = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "JobApplication not found"
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            if application.is_approve:
                if data['type'] == 'checkin' and application.in_time is None:
                    application.in_time = timezone.now()
                    application.checkin_location = data['location']
                    application.save()
                    response_data = {
                        "status": status.HTTP_200_OK,
                        "success": True,
                        "message": "Shift checked in successfully",
                        # "data": JobApplicationSerializer(application).data
                    }
                    # send notification to the client 
                    notification = Notification.objects.create(
                        user=application.vacancy.job.company.user,
                        message=f'{staff} has checked in for {application.vacancy.job_title}! Approve the checkin request.'
                    )
                    return Response(response_data, status=status.HTTP_200_OK)
                elif data['type'] == 'checkout' and application.out_time is None:
                    application.out_time = timezone.now()
                    application.checkout_location = data['location']
                    application.save()
                    response_data = {
                        "status": status.HTTP_200_OK,
                        "success": True,
                        "message": "Shift checked out successfully",
                        # "data": JobApplicationSerializer(application).data
                    }
                    # send notification to the client
                    notification = Notification.objects.create(
                        user=application.vacancy.job.company.user,
                        message=f'{staff} has checked out for {application.vacancy.job_title}! Approve the checkout request.'
                    )
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "success": False,
                        "message": "Shift already checked in/out"
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Invalid request"
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class ShiftRequestView(APIView):
    def get(self, request, pk=None,  *args, **kwargs):
        user = request.user
        staff = Staff.objects.filter(user=user).first()
        
        if pk:
            daily_shift = DailyShift.objects.filter(id=pk, staff=staff).first()
            if daily_shift:
                serializer = DailyShiftSerializer(daily_shift)
                response_data = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Shift request retrieved successfully",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Shift request not found"
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
        if DailyShift.objects.filter(staff=staff, status=False).exists():
            shifts = DailyShift.objects.filter(staff=staff, status=False)
            serializer = DailyShiftSerializer(shifts, many=True)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Shift requests retrieved successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "No pending shift requests found"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk=None, *args, **kwargs):
        data = request.data 

        
        daily_shift = DailyShift.objects.get(pk=pk)

        if data['type'] == 'request':
            if data['value'] == True:
                daily_shift.status = True
                daily_shift.shift_status = 'accepted'
                daily_shift.save()
                notification = Notification.objects.create(
                    user=daily_shift.shift.company.user,
                    message=f'{daily_shift.staff.user } has accepted your shift request.'
                )
                response_data = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Shift request accepted successfully",
                    "data": DailyShiftSerializer(daily_shift).data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            elif data['value'] == False:
                daily_shift.status = False
                daily_shift.shift_status = 'rejected'
                daily_shift.save()
                notification = Notification.objects.create(
                    user=daily_shift.shift.company.user,
                    message=f'{daily_shift.staff.user } has rejected your shift request.'
                )
                response_data = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Shift request rejected successfully",
                    "data": DailyShiftSerializer(daily_shift).data
                }
                
                return Response(response_data, status=status.HTTP_200_OK)

class ShiftCheckinView(APIView):
    def get(self,request, pk=None, *args, **kwargs):
        user = request.user
        staff = Staff.objects.filter(user=user).first()

        if pk:
            daily_shift = DailyShift.objects.filter(id=pk, staff=staff, status=True, checkin_status=False).first()
            if daily_shift:
                response = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Shift check-in request retrieved successfully",
                    "data": DailyShiftSerializer(daily_shift).data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Shift check-in request not found"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        # return all not checkin shift
        shifts = DailyShift.objects.filter(staff=staff, status=True, checkin_status=False)
        serializer = DailyShiftSerializer(shifts, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Shift check-in requests retrieved successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None, *args, **kwargs):
        data = request.data
        daily_shift = DailyShift.objects.get(pk=pk)
        if data['type'] == 'checkin':
            # daily_shift.checkin_status = True # client approve it 
            daily_shift.checkin_time = timezone.now()
            daily_shift.checkin_location = data['checkin_location']
            daily_shift.save()
            notification = Notification.objects.create(
                user=daily_shift.shift.company.user,
                message=f'{daily_shift.staff.user } has checked-in for your shift.'
            )
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Shift check-in request accepted successfully",
                # "data": DailyShiftSerializer(daily_shift).data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Invalid type. Expected 'checkin' or 'checkout'"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class ShiftCheckoutView(APIView):
    def get(self,request, pk=None, *args, **kwargs):
        user = request.user
        staff = Staff.objects.filter(user=user).first()
        if pk:
            daily_shift = DailyShift.objects.filter(id=pk, checkout_status=False).first()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Shift check-out request retrieved successfully",
                "data": DailyShiftSerializer(daily_shift).data
            }
            return Response(response, status=status.HTTP_200_OK)
        # return all not checkout shift
        shifts = DailyShift.objects.filter(staff=staff, checkout_status=False)
        serializer = DailyShiftSerializer(shifts, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Shift check-out requests retrieved successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None, *args, **kwargs):
        data = request.data
        daily_shift = DailyShift.objects.get(pk=pk)
        if data['type'] == 'checkout':
            # daily_shift.checkout_status = True # client approve it 
            daily_shift.checkout_time = timezone.now()
            daily_shift.checkout_location = data['checkout_location']
            daily_shift.save()
            notification = Notification.objects.create(
                user=daily_shift.shift.company.user,
                message=f'{daily_shift.staff.user } has checked-out for your shift.'
            )
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Shift check-out request accepted successfully",
                # "data": DailyShiftSerializer(daily_shift).data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Invalid type. Expected 'checkin' or 'checkout'"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    

# client shift 
class StaffShiftView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        user = request.user
        try:
            staff = Staff.objects.get(user=user)
        except Staff.DoesNotExist:
            response_data = {
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Staff not found"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        if staff.is_letme_staff:
            myshift = DailyShift.objects.filter(staff=staff)
            serializer = DailyShiftSerializer(myshift, many=True)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Shift records retrieved successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            try:
                mystaff = MyStaff.objects.get(staff=staff)
            except MyStaff.DoesNotExist:
                response_data = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Your staff record not found"
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            try:
                myshift, created = Shifting.objects.get_or_create(shift_for=mystaff, company=mystaff.client )

                if myshift.shifts.count() > 0:
                    shifts = myshift.dailyshift_set.all()
                else:
                    response_data = {
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": "No shift records found"
                    }
                    return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            except Shifting.DoesNotExist:
                response_data = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Your shifting record not found"
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            
            # shifts = DailyShift.objects.filter(shift=shifts)
            serializer = DailyShiftSerializer(shifts, many=True)
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Shift records retrieved successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

class ExperienceView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        user = request.user
        
        if pk is not None:
            try:
                experience = Experience.objects.get(id=pk)
                if experience.user == user:
                    serializer = ExperienceSerializer(experience)
                    response_data = {
                        "status": status.HTTP_200_OK,
                        "success": True,
                        "message": "Experience record retrieved successfully",
                        "data": serializer.data
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
            except Experience.DoesNotExist:
                response_data = {
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Experience record not found"
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        experiences = Experience.objects.filter(user=user)
        serializers = ExperienceSerializer(experiences, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Experience records retrieved successfully",
            "data": serializers.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save(user=user)
            # if user have staff then add it in experience list 
            if user.is_staff:
                staff = Staff.objects.filter(user=user).first()
                if staff:
                    staff.experience.add(obj)
            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Experience record created successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
