from rest_framework import serializers


from .models import (
    Staff,
    Experience, 
    BankDetails,
)
from users.models import User, JobRole, Skill
from users.serializers import UserSerializer, SkillSerializer

class CreateStaffSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    user_data = serializers.JSONField(write_only=True, required=False, allow_null=True)
    bank_details = serializers.JSONField(write_only=True, required=False, allow_null=True)
    # experience = serializers.PrimaryKeyRelatedField(queryset=Experience.objects.all(), many=True)

    class Meta:
        model = Staff
        fields = ['user_data','dob', 'address', 'phone', 'cv', 'video_cv', 'role','nid_number', 'about','skills', 'bank_details']


    def create(self, validated_data):
        skills = validated_data.pop('skills', [])
        experience = validated_data.pop('experience', [])
        bank_details = validated_data.pop('bank_details',None)

        user = self.context['request'].user
        user_data = validated_data.pop('user_data')
        # save staff profile 
        staff_profile = Staff.objects.create(user=user,**validated_data)
        # check if any value in skills have 
        staff_profile.skills.set(skills)

        # bank details 
        if bank_details is not None:
            bank, created = BankDetails.objects.get_or_create(staff=staff_profile,**bank_details)
        
        return staff_profile
    # update staff profile
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user_data')
        skills = validated_data.pop('skills', [])
        # update user data
        # Update user data
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update staff data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.user = user
        instance.save()

        # update skills
        if len(skills) > 0:
            instance.skills.clear()
            instance.skills.set(skills)
        
        return instance
        


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # skills = SkillSerializer(many=True, read_only=True)
    # role = StaffRoleSerializer(read_only=True)
    class Meta:
        model = Staff
        fields = '__all__'
        depth = 1
    