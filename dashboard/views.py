from django.shortcuts import render

from rest_framework import status, generics 
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .models import FavouriteStaff
from . serializers import FavouriteStaffSerializer

from client.models import CompanyProfile
from staff.models import Staff


class FavouriteStaffView(APIView):
    def get(self, request,company_id=None,pk=None):
        if pk:
            favourite = FavouriteStaff.objects.filter(staff__id=pk).first()
            if favourite:
                serializer = FavouriteStaffSerializer(favourite)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            favourites = FavouriteStaff.objects.filter(company__id=company_id)
            serializer = FavouriteStaffSerializer(favourites, many=True)
            return Response(serializer.data)
        
    def post(self, request,company_id=None, pk=None):
        data = request.data
        company = CompanyProfile.objects.filter(id=company_id).first()
        staff = Staff.objects.filter(id=data['staff_id']).first()
        favourite_staff,_ = FavouriteStaff.objects.get_or_create(company=company)

        if not company or not staff:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if data['action'] == 'add':
            favourite_staff.staff.add(staff)
            return Response({"message": "Favourite staff added successfully"})
        elif data['action'] =='remove':
            if staff in favourite_staff.staff.all():
                favourite_staff.staff.remove(staff)

            return Response({"message": "Favourite staff removed successfully"})
        
