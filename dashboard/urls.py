from django.urls import path 
from . import views 

urlpatterns = [
    path('company/jobs/vacancy/<int:vacancy_id>/review/', views.CompanyReviewView.as_view()),
    path('company/jobs/staff/<int:staff_id>/review/', views.StaffReviewView.as_view()),
    path('dashboard/notifications/', views.NotificationView.as_view()),
    path('dashboard/skills/', views.SkillView.as_view()),

    path('dashboard/jobs/', views.FeedJobView.as_view()),
    
    
]