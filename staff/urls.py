from django.urls import path 
from . import views 

urlpatterns =[
    path('staff/profile/', views.StaffProfileView.as_view()),
    path('staff/profile/<int:pk>/', views.StaffProfileView.as_view()),

]