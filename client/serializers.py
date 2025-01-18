from rest_framework import serializers
from django.shortcuts import get_object_or_404

from users.serializers import SkillSerializer, JobRoleSerializer, UniformSerializer
from users.models import Skill

from django.contrib.auth import get_user_model

from .models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy,
    JobApplication,
    StaffInvitation



)
from users.models import (
    JobRole,
    Skill,
    Uniform,

)

from dashboard.models import FavouriteStaff, Notification

from users.serializers import UserSerializer
from staff.serializers import StaffSerializer
from staff.models import Staff

User = get_user_model()

class CompanyProfileSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    class Meta:
        model = CompanyProfile
        fields = '__all__'
        read_only_fields = ['user']
    
    def get_user_info(self, obj):
        return UserSerializer(obj.user).data
        


class JobTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTemplate
        fields = '__all__'
        # read_only_fields = ['profile']

class JobSerializerForVacancy(serializers.ModelSerializer):
    company = CompanyProfileSerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'status', 'company']

class VacancySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Vacancy
        fields = '__all__'
        depth = 1

        # fields = ['user', 'job_title','number_of_staff', 'skills', 'uniform','open_date','close_date', 'start_time', 'end_time','salary', 'participants', 'staff_ids','jobs']

    


class CreateVacancySerializers(serializers.ModelSerializer):
    job_title = serializers.PrimaryKeyRelatedField(queryset=JobRole.objects.all())
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    uniform = serializers.PrimaryKeyRelatedField(queryset=Uniform.objects.all())
    invited_staff = serializers.ListField(write_only=True)
    # participants = serializers.PrimaryKeyRelatedField(queryset=FavouriteStaff.objects.all(), many=True)

    class Meta:
        model = Vacancy
        fields = ['user', 'job_title','number_of_staff','skills','uniform', 'open_date', 'close_date', 'start_time', 'end_time', 'invited_staff']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        print('validated data', validated_data)

        user = self.context['request'].user
        validated_data['user'] = user

        job_title = validated_data.pop('job_title')
        skills = validated_data.pop('skills')
        uniform = validated_data.pop('uniform')
        invited_staff_ids = validated_data.pop('invited_staff', [])
        print('invited_staff_ids:', invited_staff_ids)
        # participants = validated_data.pop('participants')
        # print('participants', participants)

        
        vacancy = Vacancy.objects.create(
            job_title=job_title,
            uniform=uniform,
            # participants=participants,
            **validated_data
        )
        vacancy.skills.set(skills)

        for invited in invited_staff_ids:
            fav_staff = FavouriteStaff.objects.filter(id=invited).first()
            print('invited staff', fav_staff)
            StaffInvitation.objects.create(vacancy=vacancy,staff=fav_staff.staff)
            # send notification
            notification = Notification.objects.create(
                user = user,
                message = f"{user.companyprofile.company_name} has invited you to a {vacancy.job_title} job application."
            )


        return vacancy
    
    # update
    

class JobSerializer(serializers.ModelSerializer):
    # vacancy = CreateVacancySerializers(many=True, write_only=True)
    # get a extra field that get a objects
    # vacancies = serializers.JSONField()
    vacancies = serializers.ListField(
        child=serializers.JSONField(),
        write_only=True  # Use only for write operations
    )
    
    class Meta:
        model = Job
        fields = ['id','company' , 'title', 'description', 'status', 'save_template', 'vacancies']
    
    # to represantation for showing all the vacancy serializers data
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add the vacancy serializers data to the data
        data['vacancy'] = VacancySerializer(instance.vacancy, many=True).data
        return data

    
    def create(self, validated_data):
        print('validated data', validated_data)
        user_ = self.context['request'].user
        print('job user', user_)
        vacancy_data = validated_data.pop('vacancies')
        print('vacancy data', vacancy_data)
        save_in_template = validated_data.get('save_template', False)
        
        job = Job.objects.create(**validated_data)
        for vacancy in vacancy_data:
            # print('vacancy', vacancy,)
            # vacancy['user'] =  user_.id
            vacancy_serializer = CreateVacancySerializers(data=vacancy, context=self.context)
            if vacancy_serializer.is_valid():
                vacancy_instance = vacancy_serializer.save()
                job.vacancy.add(vacancy_instance)
            else:
                print('serializer is not valid:', vacancy_serializer.errors)
                # return None
        # in save in tamplate true save job in template model
        #job template have user and job field with foreign key relation
        if save_in_template:
            job_template = JobTemplate.objects.create(user=user_, job=job)
            job_template.save()

        return job
    
    


class JobApplicationSerializer(serializers.ModelSerializer):
    vacancy = serializers.PrimaryKeyRelatedField(queryset=Vacancy.objects.all())
    applicant = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all())

    class Meta:
        model = JobApplication
        fields = '__all__'
   
    def create(self, validated_data):
        print('validated data', validated_data)

        return 0
