from rest_framework import serializers

from .models import (
    Staff
)



class StaffSerializer(serializers.ModelSerializer):
    # user = 
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ['user']
        
