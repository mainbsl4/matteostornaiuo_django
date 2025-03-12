from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from django.contrib.auth import get_user_model
from .models import Staff, BankDetails, Experience, StaffReview


User = get_user_model()


# bank details inline 

class BankDetailsInline(StackedInline):
    model = BankDetails
    extra = 1
    fields = ('card_holder_name', 'account_number')
    readonly_fields = ('card_holder_name', 'account_number')

# experience details inline

class ExperienceInline(StackedInline):
    model = Experience
    extra = 1
    fields = ('job_role','start_date', 'end_date', 'duration')
    readonly_fields = ('job_role','start_date', 'end_date', 'duration')
    ordering = ['-start_date']

@admin.register(Staff)
class StaffAdmin(ModelAdmin):
    list_display = ('user__first_name','user__last_name', 'phone','role','nid_number','age','gender','country','is_letme_staff','created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone','role__name','gender', 'country')
    list_filter = ('role__name', 'gender','country', 'is_letme_staff', )
    list_filter_sheet = False
    list_per_page = 50
    list_display_links = ('user__first_name','user__last_name')
    inlines = [BankDetailsInline]

    def get_changelist_instance(self, request):
        cl = super().get_changelist_instance(request)
        for filter_spec in cl.filter_specs:
            if filter_spec.field_path == "role__name":  # Use `field_path` instead
                filter_spec.title = "role " 
        return cl

    


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
