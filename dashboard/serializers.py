from rest_framework import serializers 

from .models import FavouriteStaff, CompanyReview, StaffReview, Notification
from staff.serializers import StaffSerializer

from users.models import Skill

class FavouriteStaffSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(many=True)
    class Meta:
        model = FavouriteStaff
        fields = "__all__"

class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        exclude = ('created_at',)
        read_only_fields = ['staff', 'profile', 'vacancy']
        # depth = 2
class StaffReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffReview
        exclude = ('created_at',)
        read_only_fields = ['staff', 'profile', 'vacancy']
        # depth = 2

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"