from django.urls import path 
from . import views 

urlpatterns = [
    path('company/<int:company_id>/staff/favourites/', views.FavouriteStaffView.as_view()),
    path('company/<int:company_id>/staff/favourites/<int:pk>/', views.FavouriteStaffView.as_view()),
    path('company/<int:company_id>/staff/favourites/', views.FavouriteStaffView.as_view()),
    path('company/jobs/vacancy/<int:vacancy_id>/review/', views.CompanyReviewView.as_view()),
    path('company/jobs/staff/<int:staff_id>/review/', views.StaffReviewView.as_view()),
]