from rest_framework import serializers 

from .models import FavouriteStaff
from staff.serializers import StaffSerializer

class FavouriteStaffSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(many=True)
    class Meta:
        model = FavouriteStaff
        fields = "__all__"