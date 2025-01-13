from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
from staff.models import Staff
from client.models import CompanyProfile


class FavouriteStaff(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    staff = models.ManyToManyField(Staff, related_name='favourite_staff', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Favourite Staff'
        ordering = ['-created_at']
        # unique_together = (('company', 'staff'),)
    
    def __str__(self):
        return f'{self.company.company_name}'