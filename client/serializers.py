from rest_framework import serializers,status 
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from datetime import datetime

from users.serializers import SkillSerializer, JobRoleSerializer, UniformSerializer
from users.models import Skill

from django.contrib.auth import get_user_model

from .models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy,
    JobApplication,
    Checkin,
    Checkout,
    JobAds,
    FavouriteStaff,
    MyStaff

)
from users.models import (
    JobRole,
    Skill,
    Uniform,

)

from dashboard.models import  Notification

from users.serializers import UserSerializer

from staff.serializers import StaffSerializer
from staff.models import Staff

User = get_user_model()

# done
class CompanyProfileSerializer(serializers.ModelSerializer):
    user_data = serializers.JSONField(write_only=True, required=False, allow_null=True)
    class Meta:
        model = CompanyProfile
        # fields = '__all__'
        exclude = ['created_at','updated_at']
        read_only_fields = ['user']
    
    # to_representation method for user 
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(instance.user).data
        return data
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user_data', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        return super().update(instance, validated_data)

class JobTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTemplate
        fields = '__all__'
        # read_only_fields = ['profile']


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = "__all__"
        depth = 2
    
    



class CreateVacancySerializers(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    job_title = serializers.PrimaryKeyRelatedField(queryset=JobRole.objects.all())
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, required=False)
    uniform = serializers.PrimaryKeyRelatedField(queryset=Uniform.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Vacancy
        fields = ['id','job','job_title','number_of_staff','skills','uniform', 'open_date', 'close_date', 'start_time', 'end_time','location', 'job_status']

    
    def create(self, validated_data):
        skills = validated_data.pop('skills',[])
        # invited_staff_ids = validated_data.pop('invited_staff', [])
        vacancy = Vacancy.objects.create(
            **validated_data
        )
        vacancy.skills.set(skills)

        return vacancy
class JobSerializer(serializers.ModelSerializer):
    vacancy_data = serializers.ListField(
        write_only=True 
    )
    vacancies = VacancySerializer(read_only=True, many=True)
    
    class Meta:
        model = Job
        fields = ['id','company' , 'title', 'description', 'status', 'save_template', 'vacancies', 'vacancy_data']
        read_only_fields = ['company']
        depth = 1    

    def create(self, validated_data):
        user = self.context['request'].user
        vacancy_data = validated_data.pop('vacancy_data',[])
        save_in_template = validated_data.get('save_template')
        # user must be is client
        if not user.is_client:
            return serializers.ValidationError("Only clients can update jobs.")
        client = CompanyProfile.objects.filter(user=user).first()
        validated_data['company'] = client
        
        job = Job.objects.create(**validated_data)
        
        for vacancy in vacancy_data:
            vacancy['job'] = job.id
            vacancy_serializer = CreateVacancySerializers(data=vacancy)
            if vacancy_serializer.is_valid():
                vacancy_serializer.save()
            else:
                # raise error
                return Response(vacancy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if save_in_template:
            JobTemplate.objects.create(client=user.profiles, job=job)

        return job
    def update(self, instance, validated_data):
        user_ = self.context['request'].user
        vacancy_data = validated_data.pop('vacancy_data',[])
        save_in_template = validated_data.get('save_template',False)

        if not user_.is_client:
            raise serializers.ValidationError("Only clients can update jobs.")
        client = CompanyProfile.objects.filter(user=user_).first()
        validated_data['company'] = client

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if vacancy_data:
            for vacancy_item in vacancy_data:
                vacancy_id = vacancy_item.get('id', None)
                if vacancy_id is not None:
                    vacancy_obj = Vacancy.objects.filter(id=vacancy_id).first()

                    if not vacancy_obj:
                        vacancy_id = None

                    # update vacancy using vacancy serializer 
                    vacancy_serializer = CreateVacancySerializers(instance=vacancy_obj, data=vacancy_item, partial=True)
                    if vacancy_serializer.is_valid():
                        vacancy_serializer.save()
                    else:
                        # raise error
                        raise serializers.ValidationError(vacancy_serializer.errors)
                else:
                    print('instance', instance, instance.pk)
                    # create new vacancy
                    vacancy_item['job'] = instance.id
                    vacancy_serializer = CreateVacancySerializers(data=vacancy_item)
                    if vacancy_serializer.is_valid():
                        vacancy_serializer.save()
                    else:
                        # raise error
                        raise serializers.ValidationError(vacancy_serializer.errors)
                    
                    
        if save_in_template:
            job_template, created = JobTemplate.objects.get_or_create(client=user_.profiles, job=instance)
            if created:
                job_template.user = user_
                job_template.job = instance
                job_template.save()

        return instance
    
    
class JobViewSerializers(serializers.ModelSerializer):
    company  = CompanyProfileSerializer(read_only=True)
    class Meta:
        model = Job
        exclude = ('vacancy',)


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['vacancy'] = VacancySerializer(instance.vacancy).data
        data['applicant'] = StaffSerializer(instance.applicant).data
        return data


class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkin
        exclude = ('created_at',)
        read_only_fields = ['staff']
        depth = 1
    
    
class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        exclude = ('created_at',)
        read_only_fields = ['staff']
        depth = 1


class PermanentJobsSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(),many=True, write_only=True)
    company = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = JobAds
        fields = '__all__'
        read_only_fields = ['company']
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['skills'] = SkillSerializer(instance.skills, many=True).data
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_client:
            return None
        skills = validated_data.pop('skills',{})
        
        client = CompanyProfile.objects.filter(user=user).first()
        validated_data['company'] = client
        
        job_ads = JobAds.objects.create(**validated_data)
        job_ads.skills.set(skills)
        return job_ads
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if not user.is_client:
            return None
        
        # Get the CompanyProfile for the user
        client = CompanyProfile.objects.filter(user=user).first()
        validated_data['company'] = client

        # Extract skills from validated_data
        skills = validated_data.pop('skills', None)

        # Get the instance of JobAds
        jobads = JobAds.objects.get(pk=instance.pk)
        if jobads:
            for attr, value in validated_data.items():
                setattr(jobads, attr, value)
            
            # Update skills if provided
            if skills is not None:
                jobads.skills.set(skills)

            # Save the updated instance
            jobads.save()

            return jobads

        return None
        
    

class FavouriteStaffSerializer(serializers.ModelSerializer):
    staff = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = FavouriteStaff
        fields = "__all__"
    

class MyStaffSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    client = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = MyStaff
        fields = '__all__'

class JobTemplateSserializers(serializers.Serializer):
    name = serializers.StringRelatedField(read_only=True)
    client = CompanyProfileSerializer(read_only=True)
    job = JobSerializer(read_only=True)
