from django.shortcuts import render, HttpResponse

from users.models import User
from client.models import CompanyProfile

def home(request):
    # return HttpResponse("jkldsf")
    return render(request, 'home.html')


def dashboard_callback(request, context):
    totalUsers = User.objects.count()
    totalSuperusers = User.objects.filter(is_superuser=True).count()
    totalclients = User.objects.filter(is_client=True).count()
    totalstaff = User.objects.filter(is_staff=True).count()
    context.update(
        {
            "total_users": totalUsers,
            "total_superusers": totalSuperusers,
            "total_clients": totalclients,
            "total_staff": totalstaff,
        }
    )

    return context
