from django.urls import path 
from . import views 

urlpatterns =[
    path('staff/profile/', views.StaffProfileView.as_view()),
    path('staff/profile/<int:pk>/', views.StaffProfileView.as_view()),
    # apply to the job
    
    path('staff/job/apply/', views.JobApplicationView.as_view()), #post
    path('staff/job/apply/<int:pk>/', views.JobApplicationView.as_view()), #post
    # upcoming jobs, checkin and checkout 
    path('staff/jobs/', views.JobCheckinView.as_view()), # assigned list 
    path('staff/jobs/<int:pk>/', views.JobCheckinView.as_view()),
    path('staff/jobs/<int:pk>/checkin/', views.JobCheckinView.as_view()),
    path('staff/jobs/<int:pk>/checkout/', views.JobCheckinView.as_view()),

    path('staff/reviews/', views.StaffReviewView.as_view()), #post
    path('vacancy/<int:application_id>/review/', views.StaffReviewView.as_view()), #post
    



    path('myshift/', views.StaffShiftView.as_view()), # 1

    path('staff/shift/checkin/', views.ShiftCheckinView.as_view()), # checkin details
    path('staff/shift/checkin/<int:pk>/', views.ShiftCheckinView.as_view()), # checkin details
    
    path('staff/shift/', views.ShiftRequestView.as_view()), # all shift
    path('staff/shift/<int:pk>/', views.ShiftRequestView.as_view()), # shift details

    path('staff/shift/<int:pk>/checkin/', views.ShiftCheckinView.as_view()), # checkin details
    
    path('staff/shift/<int:pk>/checkout/', views.ShiftCheckoutView.as_view()), # checkin details
    path('staff/shift/checkout/', views.ShiftCheckoutView.as_view()), # checkin details

    # path('action/job/application/<int:pk>/', views.JobApplicationView.as_view()),

    path('staff/experiences/', views.ExperienceView.as_view()),
    path('staff/experiences/<int:pk>/', views.ExperienceView.as_view()),

    # working hours
    path('staff/workinghours/<int:staff_id>/', views.StaffWorkingHoursView.as_view()),


]

