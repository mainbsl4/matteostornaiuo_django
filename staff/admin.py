from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from django.contrib.auth import get_user_model
from .models import Staff, BankDetails, Experience, StaffReview


User = get_user_model()



@admin.register(Staff)
class StaffAdmin(ModelAdmin):
    list_display = ('user', 'phone','created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone')
    


@admin.register(BankDetails)
class BankDetailsAdmin(ModelAdmin):
    list_display = ('staff', 'card_holder_name','account_number')

@admin.register(Experience)
class ExperienceAdmin(ModelAdmin):
    list_display = ('user','job_role', 'start_date', 'end_date', 'duration')


@admin.register(StaffReview)
class StaffReviewAdmin(ModelAdmin):
    list_display = ('staff', 'job_role',"review_by__company_name", 'rating', 'content', 'created_at')
    list_filter = ('staff', 'job_role', 'review_by__company_name')
    search_fields = ('staff__user__first_name', 'staff__user__last_name', 'staff__user__email', 'job_role', 'review_by__company_name')
    list_filter_sheet = False
    list_per_page = 50
    search_help_text = "Search by staff name and company name"
