from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin, StackedInline

from . models import (
    DailyShift,
    Shifting
)

@admin.register(DailyShift)
class DailyShiftAdmin(ModelAdmin):
    list_display = ('shift','staff', 'day', 'start_time','end_time' , 'status','location') 


@admin.register(Shifting)
class ShiftingAdmin(ModelAdmin):
    list_display = ('company', 'shift_for')



