from rest_framework import serializers


from .models import (
    Staff
)
from users.models import User
from users.serializers import UserSerializer

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)
    
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ['user']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if user_data:
            user_instance = instance.user

            user_instance.first_name = user_data.get('first_name', user_instance.first_name)
            user_instance.last_name = user_data.get('last_name', user_instance.last_name)            
            user_instance.save()  
        instance.save()
        return instance

        
    