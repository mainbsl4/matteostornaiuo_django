from django.contrib import admin
from unfold.admin import ModelAdmin



from .models import Packages, Subscription


@admin.register(Packages)
class PackageAdmin(ModelAdmin):
    list_display = ('name', 'price', 'number_of_staff', 'duration', 'is_active', 'created_at')

@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    pass 
