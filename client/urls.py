from django.urls import path
from . import views

urlpatterns = [
    # company profile
    path('company/profile/', views.CompanyProfileCreateView.as_view(), name='company_profile'), # read, create
    path('company/profile/<int:pk>/', views.CompanyProfileCreateView.as_view()), # put, delete
    # vacancy
    path('company/vacancy/', views.VacancyView.as_view(), name='company_vacancy'),
    path('company/vacancy/<int:pk>/', views.VacancyView.as_view()),
    # jobs
    path('company/jobs/', views.JobView.as_view()), 
    path('company/jobs/<int:pk>/', views.JobView.as_view()),
    # favourite staff 
    path('company/staff/favourites/', views.FavouriteStaffView.as_view()),
    path('company/staff/favourites/<int:pk>/', views.FavouriteStaffView.as_view()),
    # my staff
    path('company/staff/own/', views.MyStaffView.as_view()),
    path('company/staff/own/<int:pk>/', views.MyStaffView.as_view()),
    # job application
    path('client/job/<int:vacancy_id>/applications/', views.JobApplicationAPI.as_view()), # post request from staff 
    path('client/job/<int:vacancy_id>/applications/<int:pk>/', views.JobApplicationAPI.as_view()),
    # application approve
    path('company/jobs/applications/<int:application_id>/add/', views.AcceptApplicantView.as_view()),
    path('company/jobs/vacancy/<int:vacancy_id>/checkin/', views.CheckInView.as_view()),
    path('company/jobs/vacancy/<int:vacancy_id>/checkout/', views.CheckOutView.as_view()),
    # checkin application
    path('company/jobs/vacancy/<int:vacancy_id>/checkin/approve/', views.ApproveCheckinView.as_view()),
    path('company/jobs/vacancy/<int:vacancy_id>/checkout/approve/', views.ApproveCheckoutView.as_view()),
    # job ads
    path('company/job/ads/', views.JobAdsView.as_view()),
    path('company/job/ads/<int:pk>/', views.JobAdsView.as_view()),
    # shifting
    path('company/shifting/<int:shifting_id>/request/', views.ShiftCheckinAcceptView.as_view()),
    path('company/shifting/<int:shifting_id>/accept/<int:pk>/', views.ShiftCheckinAcceptView.as_view()),



]