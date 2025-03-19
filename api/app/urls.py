from django.urls import path, include

urlpatterns = [
    path('app/', include('users.urls')),
    path('app/', include('client.urls') ),
    path('app/', include('staff.urls')),
    path('app/', include('dashboard.urls')),
    path('app/', include('chat.urls')),
    path('app/', include('shifting.urls')),
    path('app/', include('subscription.urls')),
    path('app/', include('homedashbord.urls')),
    path('app/', include('celeryapi.urls')),
]