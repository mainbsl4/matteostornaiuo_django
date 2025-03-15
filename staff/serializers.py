from rest_framework import serializers

from django.db.models import Avg, Count

from .models import (
    Staff,
    Experience, 
    BankDetails,
    StaffReview
    
)

from users.models import User, JobRole, Skill
from users.serializers import UserSerializer, SkillSerializer, JobRoleSerializer
class CreateStaffSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    experience = serializers.PrimaryKeyRelatedField(queryset=Experience.objects.all(), many=True)
    user_data = serializers.JSONField(write_only=True, required=False, allow_null=True)
    bank_details = serializers.JSONField(write_only=True, required=False, allow_null=True)
    # experience = serializers.PrimaryKeyRelatedField(queryset=Experience.objects.all(), many=True)

    class Meta:
        model = Staff
        fields = ['user_data','dob', 'address', 'phone', 'cv', 'video_cv', 'role','nid_number', 'gender','about','country','post_code','skills', 'bank_details', 'experience']


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
        staff_profile.experience.set(experience)
    
        # bank details 
        if bank_details is not None:
            bank, created = BankDetails.objects.get_or_create(staff=staff_profile,**bank_details)
        
        return staff_profile
    # update staff profile
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user_data')
        skills = validated_data.pop('skills', [])
        experience = validated_data.pop('experience', [])
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
        
        # update experience
        if len(experience) > 0:
            instance.experience.clear()
            instance.experience.set(experience)
        
        return instance
        
class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = '__all__'
        # depth = 1

class ExperienceSerializer(serializers.ModelSerializer):
    job_role = serializers.PrimaryKeyRelatedField(queryset = JobRole.objects.all())
    class Meta:
        model = Experience
        fields = '__all__'
        # depth = 1
        read_only_fields = ['user']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['job_role'] = JobRoleSerializer(instance.job_role).data
        return data

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avg_rating = serializers.SerializerMethodField(read_only=True, required=False)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)  # Get dynamic fields if provided
        super().__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    class Meta:
        model = Staff
        fields = ['id','user', 'avg_rating','role', 'nid_number', 'phone', 'address', 'dob', 'age', 'avatar', 'about', 'cv', 'video_cv','skills','is_available','is_letme_staff']
        depth = 1
    
    def get_avg_rating(self, obj):

        total_avg = StaffReview.objects.filter(staff=obj).aggregate(total_avg_rating=Avg('rating'))['total_avg_rating']

        rating = (
            StaffReview.objects
            .filter(staff=obj)
            .values('job_role')
            .annotate(
                avg_rating=Avg('rating'), 
                review_count=Count('id') 
            )
        )

        return {
            'total_avg_rating': total_avg,  
            'job_role_ratings': list(rating)  
        }

class StaffReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffReview
        fields = '__all__'
        