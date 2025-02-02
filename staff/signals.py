from django.db.models.signals import post_save
from django.dispatch import receiver 
from .models import Staff
from users.models import Invitation
from client.models import MyStaff, CompanyProfile


@receiver(post_save, sender=Staff)
def add_staff_to_mystaff(sender, instance, created, **kwargs):
    if created:
        invitation = Invitation.objects.filter(staff_email=instance.user.email).first()
        if invitation:
            invited_by = invitation.staff_invitation.user
            client = CompanyProfile.objects.filter(user=invited_by).first()
            MyStaff.objects.create(staff=instance, client=client, status=True)
            # send email to invited staff
