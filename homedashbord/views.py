from django.shortcuts import render

from users.models import User
from client.models import CompanyProfile


def dashboard_callback(request, context):
    context.update(
        {
            "total_users": "rrrrrrrrrrrrrrr",
        }
    )

    return context
