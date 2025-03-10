from django.shortcuts import render
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# Create your views here.
from .serializers import StaffInfoSerializer
from staff.models import Staff
from client.models import JobApplication



class StaffToCelery(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        staffs = Staff.objects.all()
        serializer = StaffInfoSerializer(staffs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StaffPaymentCeleryAPI(APIView):

    def get(self, request):
        applications = JobApplication.objects.filter(checkout_approve=True)
        payment_lists = []
        for application in applications:
            seconds = application.total_working_hours.total_seconds()
            print(seconds, type(seconds))
            hours, rem = divmod(int(seconds), 3600)
            minutes, _ = divmod(rem,60)

            data = {
                "staff_id": application.applicant.id,
                "full name": application.applicant.user.first_name +" "+ application.applicant.user.last_name,
                "mail": application.applicant.user.email,
                "job id": application.vacancy.job.id,
                "job title": application.vacancy.job.title,
                "client id": application.vacancy.job.company.id,
                "staff role salary": application.applicant.role.staff_price,
                "staff role actual job": application.vacancy.job_title.name,
                "start date": application.vacancy.open_date,
                "end date": application.vacancy.close_date,
                "start time": application.vacancy.start_time,
                "end time": application.vacancy.end_time,
                # "total working hour" : f'{hours} hours {minutes} minutes',
                "total working hour" : str(application.total_working_hours),
                "total salary": float (application.jobreport_set.first().total_pay)
                
            }
            payment_lists.append(data)

        return Response(payment_lists)