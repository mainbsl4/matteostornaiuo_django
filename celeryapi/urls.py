from django.urls import path 
from . import views 

urlpatterns = [
    path('celery/staff/', views.StaffToCelery.as_view()),
    path('celery/payment/', views.StaffPaymentCeleryAPI.as_view()),

]