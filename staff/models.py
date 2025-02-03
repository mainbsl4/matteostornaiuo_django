from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


from users.models import JobRole, Skill



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
    avatar = models.ImageField(blank=True, null=True, upload_to='images/staff/avatar/')
    cv = models.FileField(blank=True, null=True, upload_to='staff/cv/')
    video_resume = models.FileField(blank=True, null=True, upload_to='staff/video_resume/')

    role = models.ManyToManyField(JobRole, blank=True, related_name='staff_roles')
    skills = models.ManyToManyField(Skill, blank=True, related_name="staff_skill")
    # review = 
    is_letme_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Staff'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} '
    # calculate age in year
    def age_in_year(self):
        from datetime import datetime
        today = datetime.now()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    # get staff role 
    # @property
    # def get_staff_role(self):
    #     return self.role.first()
    
class StaffRole(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    role = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Staff Roles'
        ordering = ['order']
        unique_together = (('staff', 'role'),)
    
    def __str__(self):
        return f'{self.staff.user.first_name} {self.staff.user.last_name} - {self.role}'
    
    

