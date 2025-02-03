from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from django.contrib.auth import get_user_model
from .models import Staff, StaffRole


User = get_user_model()


class StaffInline(StackedInline):
    model = StaffRole
    # extra = 1
@admin.register(Staff)
class StaffAdmin(ModelAdmin):
    list_display = ('user', 'phone', 'exp_year', 'created_at')
    # readonly_fields = ['user']
    inlines = [StaffInline]
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone')
    

@admin.register(StaffRole)
class StaffRoleAdmin(ModelAdmin):
    list_display = ('staff', 'role', 'order', 'is_primary')