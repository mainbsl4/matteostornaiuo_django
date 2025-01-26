from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .serializers import (
    DailyShiftSerializer,
    ShiftingSerializer,

)

from.models import (
    DailyShift,
    Shifting,

)

class DailyShiftingAPIView(APIView):
    def get(self, request):
        daily_shifts = DailyShift.objects.all()
        serializer = DailyShiftSerializer(daily_shifts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DailyShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ShiftingAPIView(APIView):
    def get(self, request, company_id=None):
        shifts = Shifting.objects.filter(company__id = company_id)
        serializer = ShiftingSerializer(shifts, many=True)
        return Response(serializer.data)


