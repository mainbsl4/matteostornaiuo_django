from django.urls import path, include

urlpatterns = [
    path('web/', include('users.urls')),
    path('web/', include('client.urls') ),
    path('web/', include('staff.urls')),
    path('web/', include('dashboard.urls')),
    path('web/', include('chat.urls')),
    path('web/', include('shifting.urls')),
    path('web/', include('subscription.urls')),
    path('web/', include('homedashbord.urls')),
    path('web/', include('celeryapi.urls')),
]