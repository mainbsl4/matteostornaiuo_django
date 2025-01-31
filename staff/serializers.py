from rest_framework import serializers


from .models import (
    Staff
)
from users.models import User, JobRole, Skill
from users.serializers import UserSerializer

    
        # depth = 1

class CreateStaffSerializer(serializers.ModelSerializer):
    role_id = serializers.CharField(max_length=2, write_only=True)
    skill_id = serializers.ListField(write_only=True, required=False)
    class Meta:
        model = Staff
        fields = ['dob', 'address', 'phone', 'exp_year', 'cv', 'video_resume', 'role_id','skill_id']

    def create(self, validated_data):
        role_id = validated_data.pop('role_id', None)
        skills = validated_data.pop('skill_id', [])

        user = self.context['request'].user
        # save staff profile 
        staff_profile = Staff.objects.create(user=user,**validated_data)
        # create a job role
        role = JobRole.objects.get(id=role_id)
        
        
        # check if any value in skills have 
        if skills:
            for skill_id in skills:
                skill = Skill.objects.get(id=skill_id)
                staff_profile.skills.add(skill)
        
        return staff_profile
        


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Staff
        fields = '__all__'

    # serializers method field for shoing staff role 
    
        
    def create(self, validated_data):
        print('validated data', validated_data)
        user = self.context['request'].user
        # extract addiotional data
        role_data = validated_data.pop('role_id', None)
        print('role_data', role_data)
        
        staff_profile = Staff.objects.create(user=user,**validated_data)

        # create a job role
        role = JobRole.objects.get(id=role_data)

        
        return staff_profile
        
        

        
    

    
    # to_representation method for showing staff profiles information
    