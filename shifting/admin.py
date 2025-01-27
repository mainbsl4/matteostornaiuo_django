from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from . models import (
    DailyShift,
    Shifting
)


class DailyShiftAdmin(ModelAdmin):
    list_display = (
        'shift',
        'staff',
        'day',
        'start_time',
        'end_time',
        'location',
        'shift_status',
        'status',
        'checkin_time',
        'checkout_time',
        'checkin_location',
        'checkout_location',
    
    )
    list_filter = (
        'shift_status',
        'status',
        'day',
    
    )
    search_fields = (
        'staff__user__first_name',
        'staff__user__last_name',
        'location',
        'shift__company__company_name',
    )
    ordering = ['-created_at']
    fieldsets = (
        ('Shift Details', {
            'fields': (
                'shift',
                'staff',
                'day',
                'start_time',
                'end_time',
                'location',
                'shift_status',
                'status',
            ),
        }),
        ('Check-in/Check-out Details', {
            'fields': (
                'checkin_time',
                'checkout_time',
                'checkin_location',
                'checkout_location',
                'checkin_status',
                'checkout_status',
            ),
        }),
        # ('Metadata', {
        #     'fields': (
        #         'created_at',
        #         'updated_at',
        #     ),
        # }),
    )
    readonly_fields = ('created_at', 'updated_at')
    list_filter_sheet = False



# Optional: Inline for related objects (if needed)
class DailyShiftInline(TabularInline):
    model = DailyShift
    extra = 1  # Number of empty forms to display


class ShiftingAdmin(ModelAdmin):
    list_display = ('company', 'shift_for', 'created_at')
    list_filter = ('company', 'created_at')
    search_fields = ('company__company_name', 'shift_for__staff__user__first_name')
    ordering = ['-created_at']
    inlines = [DailyShiftInline]  # Add DailyShift as inline


# Register models with admin
admin.site.register(DailyShift, DailyShiftAdmin)
admin.site.register(Shifting, ShiftingAdmin)


# @admin.register(DailyShift)
# class DailyShiftAdmin(ModelAdmin):
#     list_display = ('shift','staff', 'day', 'start_time','end_time' , 'status','location', 'checkin_time', 'checkout_time', 'shift_status')
#     # add filter, date hiararchy, search 
#     search_fields = ('staff', 'company', 'shift_status', 'day','location')
#     list_filter = ('shift', 'shift_status','checkin_status', 'checkout_status')
#     list_filter_sheet = False
#     date_hierarchy = 'day'
#     list_fullwidth = True
    



# @admin.register(Shifting)
# class ShiftingAdmin(admin.ModelAdmin):
#     list_display = ('company', 'shift_for')



