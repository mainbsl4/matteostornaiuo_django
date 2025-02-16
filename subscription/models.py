from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

# Create your models here.
class Packages(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    number_of_staff = models.IntegerField(default=0)
    duration = models.IntegerField(default=1)


    is_active = models.BooleanField(default=False)
    stripe_product_id = models.CharField(max_length=100, blank=True)
    stripe_price_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'
        ordering = ['-created_at']


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_subscriptoin_id = models.CharField(max_length=200,blank=True)
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='active')  # other status cancel  

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.package.name}"