from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import (
    User, 
    Skill, 
    JobRole, 
    Uniform,
    Invitation,
    StaffInvitation
    )
        
# Register your models here.

# admin.site.register(User)



# Register your models here.
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email','first_name','last_name', 'is_client', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_client', 'is_staff', 'is_active')
    search_fields = ('email','first_name','last_name')
    ordering = ('-date_joined',)
    list_per_page = 20  
    list_filter_sheet = True


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    search_fields = ('name',)
    list_per_page = 20
    # list_filter = ('name',)
    # list_filter_sheet = False 


@admin.register(JobRole)
class JobRoleAdmin(ModelAdmin):
    list_display = ('name', 'price_per_hour')
    search_fields = ('name',)
    list_filter = ('name',)
    list_per_page = 20
    list_filter_sheet = False  # Enable filter sheet


@admin.register(Uniform)
class UniformAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',) 
    list_per_page = 20
    

# @admin.register(Invitation)
# class StaffInvitationAdmin(ModelAdmin):
#     pass


class InvitationInline(TabularInline):
    model = Invitation
    extra = 1  # Number of empty forms to display
@admin.register(StaffInvitation)
class StaffInvitationAdmin(ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email',)
    inlines = [InvitationInline]
    list_per_page = 20
    ordering = ('-created_at',)  # Order by created_at descending
    list_display_links = ('user',)  # Make the user field a link

@admin.register(Invitation)
class InvitationAdmin(ModelAdmin):
    list_display = ('staff_name', 'staff_email', 'phone', 'job_role', 'employee_type')
    search_fields = ('staff_name', 'staff_email', 'phone')
    list_filter = ('job_role', 'employee_type')
    list_per_page = 20
    ordering = ('staff_name',)  
    # Order by staff_name ascending
    extra = 1