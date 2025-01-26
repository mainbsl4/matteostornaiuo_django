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


    
    # send notification to staff 
    
    


class Shifting(models.Model):
    company =  models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    shift_for = models.ForeignKey(MyStaff, on_delete=models.CASCADE)
    # shift = models.ManyToManyField(DailyShift, related_name='daily_shifts', blank=True)  

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.company.company_name} - {self.shift_for}'
    class Meta:
        verbose_name_plural = 'Shifts'
        ordering = ['-created_at']
        unique_together = (('company','shift_for'),)
        
    @property
    def set_my_shift(self):
        me = self.shift_for.staff
        self.shift.add(me)
    
class DailyShift(models.Model):
    shift = models.ForeignKey(Shifting, related_name="shifts", on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return f'{self.staff.user.first_name} {self.staff.user.last_name} - {self.day}'
    class Meta:
        verbose_name_plural = 'Daily Shifts'
        ordering = ['-created_at']