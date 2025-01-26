from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin

from . models import (
    DailyShift,
    Shifting
)

@admin.register(DailyShift)
class DailyShiftAdmin(ModelAdmin):
    pass 

@admin.register(Shifting)
class ShiftingAdmin(ModelAdmin):
    pass 
