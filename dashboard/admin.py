from django.contrib import admin

from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter

from .models import  Notification


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('user', 'created_at', 'is_read', 'message')
    list_editable = ('is_read', )


