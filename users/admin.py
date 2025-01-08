from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User, Skill
# Register your models here.

# admin.site.register(User)





# Register your models here.
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('first_name','last_name','email', 'is_client', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_client', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('-date_joined',)
    list_per_page = 20  # Number of records per page
    # list_editable = ('is_client', 'is_staff', 'is_active')


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    pass 
