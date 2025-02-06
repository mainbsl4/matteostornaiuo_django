from django.contrib import admin

from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter

from . models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy,
    JobApplication,
    StaffInvitation,
    Checkout,
    Checkin,
    JobAds,
    MyStaff, FavouriteStaff


)

@admin.register(CompanyProfile)
class CompanyProfileAdmin(ModelAdmin):
    list_display = ('company_name', 'contact_number', 'company_email','company_address')
    search_fields = ('company_name', 'contact_number', 'company_email', 'company_address')

    
class VacancyInline(TabularInline):  # or admin.StackedInline for a different layout
    model = Job.vacancy.through  # ManyToMany relation requires using `through`
    extra = 1  # Number of empty forms to display

@admin.register(Job)
class JobAdmin(ModelAdmin):
    list_display = ('title', 'company', 'status', 'created_at')
    list_filter = ('status', 'company')
    search_fields = ('title', 'description', 'company__name')
    ordering = ('-created_at',)
    inlines = [VacancyInline]
    filter_horizontal = ('vacancy',)  # Improves ManyToMany selection UI

@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    list_display = ('job_title', 'client', 'salary', 'open_date','start_time', 'close_date','end_time', 'one_day_job')
    # list_filter = ('job_title','client__company_name')
    search_fields = ('job_title__name', 'client__company_name')
    ordering = ('-created_at',)
    date_hierarchy = 'open_date'
    list_filter_sheet = False
    list_per_page = 50

    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = (
        'job_title',
        'client__company_name',
        ("open_date", RangeDateFilter),  # Date filter
        # ("close_date", RangeDateFilter),  # Date filter
    )


@admin.register(FavouriteStaff)
class FavouriteStaffAdmin(ModelAdmin):
    list_display = ('company','number_of_staff', 'created_at' ) 
    list_filter = ('company__company_name',)
    search_fields = ('company__company_name', 'staff__user__first_name', 'staff__user__last_name')
    list_filter_sheet = False 
    list_per_page = 50

    # show count of total staff
    def number_of_staff(self, obj):
        return obj.staff.count()
@admin.register(JobTemplate)
class JobTemplateAdmin(ModelAdmin):
    pass 




@admin.register(JobApplication)
class JobApplicationAdmin(ModelAdmin):
    list_display = ('applicant','vacancy__job_title', 'applicant__is_letme_staff', 'job_status',  'is_approve', 'created_at')
    list_filter = ('is_approve', 'job_status', 'created_at')
    search_fields = ('vacancy__job_title__name', 'applicant__user__first_name', 'applicant__user__email')
    list_filter_sheet = False 
    list_editable = ('is_approve',)
    
    # fieldset for checkin checout time 
    fieldsets = (
        ('Job Application Details', {
            'fields': (
                'applicant',
                'vacancy',
                'job_status',
                'is_approve',
                
            )
        }),
        ('Check-in/Check-out Details', {
            'fields': (
                'in_time',
                'out_time',
                
            ),
        })
        )

@admin.register(StaffInvitation)
class StaffInvitationAdmin(ModelAdmin):
    list_display = ('staff', 'vacancy',  'created_at', 'status')

@admin.register(Checkin)
class CheckinAdmin(ModelAdmin):
    list_display = ('staff', 'vacancy', 'in_time', 'status')
@admin.register(Checkout)
class CheckoutAdmin(ModelAdmin):
    list_display = ('staff', 'vacancy', 'out_time', 'status')

@admin.register(JobAds)
class PermanentJobsAdmin(ModelAdmin):
    list_display = ('job_title', 'company', 'start_date', 'number_of_staff', 'is_paid', 'created_at')
    list_filter_sheet = False
    list_filter = ('is_paid', 'company__company_name')
    search_fields = ('job_title', 'company__company_name')
    # horizontal filter by date
    # date_hierarchy = 'start_date'

@admin.register(MyStaff)
class MyStaffAdmin(ModelAdmin):
    list_display = ('client', 'staff', 'start_date', 'status')
    list_filter_sheet = False
    search_fields = ('client__company_name', 'staff__user__first_name', 'staff__user__last_name', 'status')
    list_filter = ('status', 'client__company_name')