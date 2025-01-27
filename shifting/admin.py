from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin, StackedInline

from . models import (
    DailyShift,
    Shifting
)

@admin.register(DailyShift)
class DailyShiftAdmin(ModelAdmin):
    list_display = ('shift','staff', 'day', 'start_time','end_time' , 'status','location', 'checkin_time', 'checkout_time', 'shift_status')
    # add filter, date hiararchy, search 
    search_fields = ('staff', 'company', 'shift_status', 'day')
    list_filter = ('shift', 'shift_status')
    list_filter_sheet = False
    date_hierarchy = 'day'
    list_fullwidth = True



@admin.register(Shifting)
class ShiftingAdmin(ModelAdmin):
    list_display = ('company', 'shift_for')



