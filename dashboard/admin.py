from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import FavouriteStaff, Notification


@admin.register(FavouriteStaff)
class FavouriteStaffAdmin(ModelAdmin):
    list_display = ('company','staff','staff__id') 

    # show number of staff
    
    

@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('user', 'created_at', 'is_read')
    list_editable = ('is_read', )
