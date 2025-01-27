from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Staff,
    StaffRole
)
from .serializers import (
    StaffSerializer,
    CreateStaffSerializer,
    StaffRoleSerializer

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
    

class StaffRoleView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = StaffRole.objects.all()
        serializer = StaffRoleSerializer(queryset, many=True)

        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Staff roles retrieved successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = StaffRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_201_CREATED,
                "message": "Staff role created successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ShiftRequestView(APIView):
    def get(self, request,  *args, **kwargs):
        user = request.user
        staff = Staff.objects.filter(user=user).first()
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

    def post(self, request, *args, **kwargs):
        data = request.data  
        daily_shift = DailyShift.objects.filter(id=data['shift']).first()
        if daily_shift and data['status'] == True:
            daily_shift.status = True
            daily_shift.save()
            # send notification to client 
            notification = Notification.objects.create(
                user = daily_shift.shift.company.user,
                message = f"Your shift request for {daily_shift.shift.shift_for.staff.staffrole_set.first().role} has been approved",
                
            )
            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Shift request approved successfully",
                "data": daily_shift.id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
