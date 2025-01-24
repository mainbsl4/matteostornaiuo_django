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
    cv = models.FileField(blank=True, null=True, upload_to='staff/cv/')
    video_resume = models.FileField(blank=True, null=True, upload_to='staff/video_resume/')
    # role = models.ManyToManyField("StaffRole", blank=True, related_name='staff_roles')
    skills = models.ManyToManyField(Skill, blank=True, related_name="staff_skill")
    # review = 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Staff'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    # calculate age in year
    def age_in_year(self):
        from datetime import datetime
        today = datetime.now()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
class StaffRole(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    role = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    comment = models.TextField(blank=True)
    primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Staff Roles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.staff.user.first_name} {self.staff.user.last_name} - {self.role}'
    

