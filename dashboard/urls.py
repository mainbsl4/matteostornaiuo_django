from django.urls import path 
from . import views 

urlpatterns = [
    path('dashboard/notifications/', views.NotificationView.as_view()),
    path('dashboard/skills/', views.SkillView.as_view()),

    path('dashboard/jobs/', views.FeedJobView.as_view()),
    path('dashboard/jobs/<int:pk>/', views.FeedJobView.as_view()),
    path('dashboard/jobs/status-count/', views.JobCountAPI.as_view()),

    path('job/templates/', views.GetJobTemplateAPIView.as_view()),
    path('job/templates/<int:pk>/', views.GetJobTemplateAPIView.as_view()),

    
]