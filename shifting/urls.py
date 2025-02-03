from django.urls import path 
from . import views 

urlpatterns = [
    path('company/shifting/shift/', views.DailyShiftingAPIView.as_view()),
    path('company/<int:company_id>/shifting/', views.ShiftingAPIView.as_view()),

]