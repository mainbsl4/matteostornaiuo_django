from django.urls import path
from . import views

urlpatterns = [
    path('company/profile/', views.CompanyProfileCreateView.as_view()),
    path('company/profile/<int:pk>/', views.CompanyProfileCreateView.as_view()),
    path('company/vacancy/', views.VacancyView.as_view()),
    path('company/vacancy/<int:pk>/', views.VacancyView.as_view()),
    path('company/jobs/', views.JobView.as_view()),
    path('company/jobs/<int:pk>/', views.JobDetailView.as_view()),


]