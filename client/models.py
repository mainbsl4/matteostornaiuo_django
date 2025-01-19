from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import Skill, Uniform, JobRole
from staff.models import Staff

User = get_user_model()

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    company_email = models.EmailField(max_length=50)
    billing_email = models.EmailField(max_length=50)
    company_address = models.CharField(max_length=200)
    company_details  = models.TextField(blank=True)
    company_logo = models.ImageField(blank=True, null=True, upload_to='images/company/logo/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # invite_staff = models.ManyToManyField(Staff, blank=True, related_name='staff')
    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = 'Company Profile'
        verbose_name_plural = 'Company Profiles'

class Vacancy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='vacancies')
    job_title = models.ForeignKey(JobRole, on_delete=models.CASCADE, blank=True)
    number_of_staff = models.IntegerField(default=1)
    skills = models.ManyToManyField(Skill, related_name='skills', blank=True)  
    uniform = models.ForeignKey(Uniform, on_delete=models.SET_NULL, blank=True, null=True)
    open_date = models.DateField()
    close_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    participants = models.ManyToManyField(Staff, related_name='participants', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.job_title.name
    
    class Meta:
        verbose_name = 'Job Vacancy'
        verbose_name_plural = 'Job Vacancy'
        ordering = ['-created_at']

    # calculate salary, jobreole ahve price per hour, salary is salary_per_hour x hours (start time and end time)
    def calculate_salary(self):
        # calculate hour form start and end time
        hours = (self.end_time.hour - self.start_time.hour) + (self.end_time.minute - self.start_time.minute) / 60
        self.salary = self.job_title.price_per_hour * hours
        return self.salary
    
    # set salary in save method
    def save(self, *args, **kwargs):
        self.calculate_salary()
        super().save(*args, **kwargs)

    

JOB_STATUS = (
    ('PUBLISHED', 'Published'),
    ('DRAFT', 'Draft'),
    ('ARCHIVED', 'Archived'),
    ('EXPIRED', 'Expired'),
    ('CLOSED', 'Closed'),
    ('WAITING_FOR_RESPONSE', 'Waiting for Response'),
)

class Job(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    vacancy = models.ManyToManyField(Vacancy, related_name='vacancies', blank=True)
    status = models.CharField(max_length=10, default='PUBLISHED')
    save_template= models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-created_at']

class JobTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job =   models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return self.job.title
    

class JobApplication(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    in_time = models.DateTimeField(blank=True, null=True)
    out_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.applicant.user.email} - {self.vacancy.job_title}'
    

class StaffInvitation(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.staff.user.email} -invited in {self.vacancy.job_title}'

class Checkin(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    in_time = models.DateTimeField()
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.staff.user.email} - checked in at {self.in_time}'

class Checkout(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    out_time = models.DateTimeField()
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.staff.user.email} - checked out at {self.out_time}'
    
