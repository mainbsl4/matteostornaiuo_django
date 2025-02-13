from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import  Notification, CompanyReview


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('user', 'created_at', 'is_read', 'message')
    list_editable = ('is_read', )

@admin.register(CompanyReview)
class CompanyReviewAdmin(ModelAdmin):
    list_display = ('profile', 'staff', 'vacancy', 'rating', 'created_at')
