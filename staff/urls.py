from django.urls import path 
from . import views 

urlpatterns =[
    path('staff/profile/', views.StaffProfileView.as_view()),
    path('staff/profile/<int:pk>/', views.StaffProfileView.as_view()),
    
    path('myshift/', views.StaffShiftView.as_view()), # 1

    path('staff/shift/checkin/', views.ShiftCheckinView.as_view()), # checkin details
    path('staff/shift/checkin/<int:pk>/', views.ShiftCheckinView.as_view()), # checkin details
    
    path('staff/shift/', views.ShiftRequestView.as_view()), # all shift
    path('staff/shift/<int:pk>/', views.ShiftRequestView.as_view()), # shift details

    path('staff/shift/<int:pk>/checkin/', views.ShiftCheckinView.as_view()), # checkin details
    
    path('staff/shift/<int:pk>/checkout/', views.ShiftCheckoutView.as_view()), # checkin details
    path('staff/shift/checkout/', views.ShiftCheckoutView.as_view()), # checkin details

    path('action/job/application/', views.JobApplicationView.as_view()),
    path('action/job/application/<int:pk>/', views.JobApplicationView.as_view()),

]

