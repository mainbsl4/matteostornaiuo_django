from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
from staff.models import Staff
from client.models import CompanyProfile


class FavouriteStaff(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Favourite Staff'
        ordering = ['-created_at']
        # unique_together = (('company', 'staff'),)
    
    def __str__(self):
        return f'{self.company.company_name}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # to whom
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Notifications'   
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.message[:20]}...'