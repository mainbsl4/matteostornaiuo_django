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
    list_display = ('email', 'first_name', 'last_name', 'is_client', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_client', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('date_joined',)
    list_per_page = 20  
    list_filter_sheet = False 
    # Note: 'list_filter_sheet' is not a valid attribute in Django admin; did you mean something else?

    # def serial_number(self, obj):
    #     """Generate a serial number for each row."""
    #     # Get the current queryset and calculate the position
    #     queryset = self.get_queryset(self.request)
    #     index = queryset.filter(pk__lte=obj.pk).count()
    #     # Adjust for pagination
    #     page = self.get_page_number()
    #     if page > 1:
    #         return ((page - 1) * self.list_per_page) + index
    #     return index

    # serial_number.short_description = 'S.No.'
    # serial_number.admin_order_field = '-date_joined'  

    # def get_queryset(self, request):
    #     """Store the request for use in serial_number."""
    #     self.request = request
    #     return super().get_queryset(request)

    # def get_page_number(self):
    #     """Helper to get the current page number from the request."""
    #     try:
    #         return int(self.request.GET.get('p', 1))  # 'p' is the pagination param in admin
    #     except ValueError:
    #         return 1











@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    search_fields = ('name',)
    list_per_page = 20
    # list_filter = ('name',)
    # list_filter_sheet = False 


@admin.register(JobRole)
class JobRoleAdmin(ModelAdmin):
    list_display = ('name', 'staff_price', 'client_price')
    search_fields = ('name',)
    list_filter = ('name',)
    list_per_page = 20
    list_filter_sheet = False  # Enable filter sheet


@admin.register(Uniform)
class UniformAdmin(ModelAdmin):
    list_display = ('name', 'job_role', 'description')
    search_fields = ('name','job_role') 
    list_filter = ('job_role',)
    list_filter_sheet = False 
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