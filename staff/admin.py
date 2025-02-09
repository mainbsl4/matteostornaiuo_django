from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from django.contrib.auth import get_user_model
from .models import Staff, BankDetails, Experience


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