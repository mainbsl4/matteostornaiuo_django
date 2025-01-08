from django.urls import path
from . import views

urlpatterns = [
    path('company/profile/', views.CompanyProfileCreateView.as_view()),
    path('company/profile/<int:pk>/', views.CompanyProfileCreateView.as_view()),
    path('company/job/template/', views.JobTemplate.as_view()),
    

]