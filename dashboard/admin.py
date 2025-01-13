from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import FavouriteStaff


@admin.register(FavouriteStaff)
class FavouriteStaffAdmin(ModelAdmin):
    pass 
