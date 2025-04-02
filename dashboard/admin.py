from django.contrib import admin

from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter

from .models import  Notification, Report, FAQ, TermsAndConditions


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('user', 'created_at', 'is_read', 'message')
    list_editable = ('is_read', )


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_display = ('user', 'type', 'created_at','is_resolved')
    # list_editable = ('type', )
    search_fields = ('user__first_name', 'user__last_name', 'type')
    list_filter = (
        ('created_at', RangeDateTimeFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
    )

@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ('question','answer')
    search_fields = ('question', 'answer')

@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(ModelAdmin):
    pass 
