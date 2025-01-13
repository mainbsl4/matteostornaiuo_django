from django.urls import path 
from . import views 

urlpatterns = [
    path('company/<int:company_id>/staff/favourites/', views.FavouriteStaffView.as_view()),
    path('company/<int:company_id>/staff/favourites/<int:pk>/', views.FavouriteStaffView.as_view()),
    path('company/<int:company_id>/staff/favourites/', views.FavouriteStaffView.as_view()),

]