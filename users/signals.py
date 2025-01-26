# add staff to mystaff after creating staff profile 
# import post_save and dispatch

from django.db.models.signals import post_save
from django.dispatch import receiver
from staff.models import Staff
