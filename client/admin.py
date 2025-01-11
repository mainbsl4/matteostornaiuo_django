from django.contrib import admin

from unfold.admin import ModelAdmin

from . models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy,

)

@admin.register(CompanyProfile)
class CompanyProfileAdmin(ModelAdmin):
    list_display = ('company_name', 'contact_number', 'company_email','company_address')


@admin.register(Job)
class JobAdmin(ModelAdmin):
    list_display = ('title', 'company_name', 'created_at')

    # company name
    def company_name(self, obj):
        return obj.company.company_name
    
@admin.register(JobTemplate)
class JobTemplateAdmin(ModelAdmin):
    pass 

@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    list_display = ('job_title','open_date','close_date' )