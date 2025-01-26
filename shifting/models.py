from django.db import models
from django.contrib.auth import get_user_model

from client.models import (
    CompanyProfile,
    Job,
    MyStaff,
)

from staff.models import (
    Staff
)
User = get_user_model()

class DailyShift(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return f'{self.staff.user.first_name} {self.staff.user.last_name} - {self.day}'
    class Meta:
        verbose_name_plural = 'Daily Shifts'
        ordering = ['-created_at']



class Shifting(models.Model):
    company =  models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    shift_for = models.OneToOneField(MyStaff, on_delete=models.CASCADE)
    shift = models.ForeignKey(DailyShift, on_delete=models.CASCADE)  

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.company.company_name} - {self.shift_for.user.first_name} {self.shift_for.user.last_name} - {self.shift_for.job_role}'
    class Meta:
        verbose_name_plural = 'Shifts'
        ordering = ['-created_at']
        unique_together = (('company','shift_for'),)
        
