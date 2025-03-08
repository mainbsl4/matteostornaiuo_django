from django.urls import path 
from . import views 

urlpatterns = [
    path('celery/staff/', views.StaffToSelery.as_view()),

]