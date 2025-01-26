from django.urls import path 
from . import views 

urlpatterns =[
    path('staff/profile/', views.StaffProfileView.as_view()),
    path('staff/profile/<int:pk>/', views.StaffProfileDetailView.as_view()),
    path('staff/profile/role/', views.StaffRoleView.as_view()),
    path('company/<int:company_id>/shift/request/', views.ShiftRequestView.as_view()),
        

]

