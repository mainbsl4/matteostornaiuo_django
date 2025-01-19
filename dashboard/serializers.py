from rest_framework import serializers 

from .models import FavouriteStaff, CompanyReview, StaffReview
from staff.serializers import StaffSerializer

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