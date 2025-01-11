from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# class Review(models.Model):
    # staff = 
    # company = 
    # rating
    # message 
    # tips_status
    # tips_amount 

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    exp_year = models.IntegerField(default=0)
    cv = models.FileField(blank=True, null=True, upload_to='staff/cv/')
    video_resume = models.FileField(blank=True, null=True, upload_to='staff/video_resume/')

    # review = 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Staff'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username}'
    # calculate age in year
    def age_in_year(self):
        from datetime import datetime
        today = datetime.now()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))