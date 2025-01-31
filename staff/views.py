from django.shortcuts import render
from django.utils import timezone

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Staff
)
from .serializers import (
    StaffSerializer,
    CreateStaffSerializer

)
from shifting.models import Shifting, DailyShift
from shifting.serializers import ShiftingSerializer, DailyShiftSerializer
from dashboard.models import Notification

class StaffProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        staff = Staff.objects.filter(user=user).first()
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
            serializer.save()
            response = {
                "status": status.HTTP_201_CREATED,
                "message": "Staff profile created successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StaffProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StaffSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Staff profile updated successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_204_NO_CONTENT,
            "success": True,
            "message": "Staff profile deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    

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
            daily_shift = DailyShift.objects.filter(id=pk, checkin_status=False).first()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Shift check-in request retrieved successfully",
                "data": DailyShiftSerializer(daily_shift).data
            }
            return Response(response, status=status.HTTP_200_OK)
        # return all not checkin shift
        shifts = DailyShift.objects.filter(staff=staff, checkin_status=False)
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