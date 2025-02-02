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
        accepted = request.query_params.get('accepted')
        if accepted and  accepted == 'true':
            daily_shifts = DailyShift.objects.filter(status=True)
            serializer = DailyShiftSerializer(daily_shifts, many=True)
            return Response(serializer.data)
        elif accepted and accepted == 'false':
            daily_shifts = DailyShift.objects.filter(status=False)
            serializer = DailyShiftSerializer(daily_shifts, many=True)
            return Response(serializer.data)
        
        
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
        # get query parameters
        accepted = request.query_params.get('accepted', None)
        # end_date = request.query_params.get('end_date', None)

        shifts = Shifting.objects.filter(company__id = company_id)
        serializer = ShiftingSerializer(shifts, many=True)
        return Response(serializer.data)


