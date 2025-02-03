from rest_framework import serializers


from .models import (
    Staff,
    StaffRole
)
from users.models import User, JobRole, Skill
from users.serializers import UserSerializer, SkillSerializer

    
class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = '__all__'
    
class CreateStaffSerializer(serializers.ModelSerializer):
    role_id = serializers.ListField(
        write_only=True,
        required=False,
        child=serializers.IntegerField()
    )
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    user_data = serializers.JSONField(write_only=True, required=False)
    class Meta:
        model = Staff
        fields = ['user_data','dob', 'address', 'phone', 'exp_year', 'cv', 'video_resume', 'role_id','skills']


    def create(self, validated_data):
        role_id = validated_data.pop('role_id',[])
        skills = validated_data.pop('skills', [])

        user = self.context['request'].user
        # save staff profile 
        staff_profile = Staff.objects.create(user=user,**validated_data)
        
        # set staff role 
        for i, role in enumerate(role_id):
            role = JobRole.objects.get(id=role)
            StaffRole.objects.get_or_create(staff=staff_profile, role=role, order=i+1)
            staff_profile.role.add(role)
        
        # check if any value in skills have 
        staff_profile.skills.set(skills)
        
        return staff_profile
    # update staff profile
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user_data')
        job_role = validated_data.pop('role_id')
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
        
        # update staff role
        if len(job_role) > 0:
            instance.role.clear()

            for i, role in enumerate(job_role):
                role = JobRole.objects.filter(id=role).first()
                if not role:
                    continue
                StaffRole.objects.get_or_create(staff=instance, role=role, order=i+1)
                instance.role.add(role)
            
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
    