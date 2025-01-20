from django.contrib import admin

from unfold.admin import ModelAdmin

from . models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy,
    JobApplication,
    StaffInvitation,
    Checkout,
    Checkin,


)

@admin.register(CompanyProfile)
class CompanyProfileAdmin(ModelAdmin):
    list_display = ('company_name', 'contact_number', 'company_email','company_address')


@admin.register(Job)
class JobAdmin(ModelAdmin):
    list_display = ('title', 'company_name', 'created_at', 'status')
    search_fields = ('title', )

    # company name
    def company_name(self, obj):
        return obj.company.company_name
    
@admin.register(JobTemplate)
class JobTemplateAdmin(ModelAdmin):
    pass 

@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    list_display = ('job_title','open_date','close_date' )
    list_filter = ('open_date','close_date' )
    search_fields = ('job_title', )
    # list_per_page = 10
    
    
    
@admin.register(JobApplication)
class JobApplicationAdmin(ModelAdmin):
    list_display = ('vacancy__job_title', 'applicant', 'created_at', 'status')

@admin.register(StaffInvitation)
class StaffInvitationAdmin(ModelAdmin):
    list_display = ('staff', 'vacancy', 'created_at', 'status')

@admin.register(Checkin)
class CheckinAdmin(ModelAdmin):
    list_display = ('staff', 'vacancy', 'in_time', 'status')
@admin.register(Checkout)
class CheckoutAdmin(ModelAdmin):
    list_display = ('staff', 'vacancy', 'out_time', 'status')

