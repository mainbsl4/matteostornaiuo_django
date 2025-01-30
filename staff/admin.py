from django.contrib import admin
from unfold.admin import ModelAdmin

from django.contrib.auth import get_user_model
from .models import Staff,StaffRole


User = get_user_model()


@admin.register(Staff)
class StaffAdmin(ModelAdmin):
    list_display = ('user', 'phone', 'exp_year', 'created_at')
    # readonly_fields = ['user']
                    

@admin.register(StaffRole)
class StaffRoleAdmin(ModelAdmin):
    list_display = ('staff', 'role', 'primary')