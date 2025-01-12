from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView




from .models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy

)
from .serializers import (
    CompanyProfileSerializer,
    JobTemplateSerializer,
    JobSerializer,
    VacancySerializer
)

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
        serializer = VacancySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class JobView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    def put(self, request, *args, **kwargs):
        job_instance = self.get_object()
        serializer = self.get_serializer(job_instance, data=request.data)
        
        if serializer.is_valid():
            self.perform_update(serializer)  # This will call the custom update method in your serializer
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    