from rest_framework import serializers,status 
from rest_framework.response import Response

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
    StaffInvitation,
    Checkin,
    Checkout,



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
    invited_staff = serializers.ListField(write_only=True, required=False )
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
    
    # update vacancy as similar create method 
    def update(self, instance, validated_data):
        print('validated data', validated_data)
        user = self.context['request'].user
        validated_data['user'] = user
        job_title = validated_data.pop('job_title')
        skills = validated_data.pop('skills')
        uniform = validated_data.pop('uniform')
        invited_staff_ids = validated_data.pop('invited_staff', [])
        print('invited_staff_ids:', invited_staff_ids)
        # participants = validated_data.pop('participants')
        # 
        instance.job_title = job_title
        instance.uniform = uniform
        # instance.participants = participants
        instance.skills.set(skills)
        instance.save()
        
        for invited in invited_staff_ids:
            fav_staff = FavouriteStaff.objects.filter(id=invited).first()
            print('invited staff', fav_staff)
            StaffInvitation.objects.create(vacancy=instance,staff=fav_staff.staff)
            # send notification
            notification = Notification.objects.create(
                user = user,
                message = f"{user.companyprofile.company_name} has invited you to a {instance.job_title} job application."
            )
        return instance
    

class JobSerializer(serializers.ModelSerializer):
    # vacancy = CreateVacancySerializers(many=True, write_only=True)
    # get a extra field that get a objects
    # vacancies = serializers.JSONField()
    vacancies = serializers.ListField(
        child=serializers.JSONField(),
        write_only=True  # Use only for write operations
    )
    # company = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Job
        fields = ['id','company' , 'title', 'description', 'status', 'save_template', 'vacancies']
    
    # to represantation for showing all the vacancy serializers data
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add the vacancy serializers data to the data
        data['vacancy'] = VacancySerializer(instance.vacancy, many=True).data
        data['company'] = CompanyProfileSerializer(instance.company, read_only=True).data
        return data


    def create(self, validated_data):
        print('validated data', validated_data)
        user_ = self.context['request'].user
        print('job user', user_)
        vacancy_data = validated_data.pop('vacancies')
        print('vacancy data', vacancy_data)
        save_in_template = validated_data.get('save_template', False)
        
        job = Job.objects.create(**validated_data)
        job_vacancies = []
        for vacancy in vacancy_data:
            # print('vacancy', vacancy,) 
            # vacancy['user'] =  user_.id
            vacancy_serializer = CreateVacancySerializers(data=vacancy, context=self.context)
            if vacancy_serializer.is_valid():
                vacancy_instance = vacancy_serializer.save()
                job_vacancies.append(vacancy_instance)
            else:
                print('serializer is not valid:', vacancy_serializer.errors)
                # return None
        # job.vacancy.add(vacancy_instance)
        job.vacancy.set(job_vacancies)
        # print('job vacancy', job.vacancy)

        #job template have user and job field with foreign key relation
        if save_in_template:
            job_template = JobTemplate.objects.create(user=user_, job=job)
            job_template.save()

        return job
    # update job alsco can update vacancy as followed create method
    def update(self, instance, validated_data):
        print('validated data', validated_data)
        user_ = self.context['request'].user
        print('job user', user_)
        vacancy_data = validated_data.pop('vacancies')
        print('vacancy data', vacancy_data)
        save_in_template = validated_data.get('save_template', False)
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        
        job_vacancies = []
        instance.vacancy.clear()
        for vacancy in vacancy_data:
            # print('vacancy', vacancy,) 
            # vacancy['user'] =  user_.id
            vacancy_serializer = CreateVacancySerializers(data=vacancy, context=self.context)
            if vacancy_serializer.is_valid():
                vacancy_instance = vacancy_serializer.save()
                job_vacancies.append(vacancy_instance)
                instance.vacancy.add(vacancy_instance)
                instance.save()
        
        #job template have user and job field with foreign key relation
        if save_in_template:
            job_template = JobTemplate.objects.create(user=user_, job=instance)
            job_template.save()
        
        return instance
    
    
    


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['vacancy'] = VacancySerializer(instance.vacancy).data
        data['applicant'] = StaffSerializer(instance.applicant).data
        return data
    def create(self, validated_data):
        print('validated data', validated_data)

        job_application = JobApplication.objects.create(**validated_data)
        # send notification to vacancy user
        vacancy = validated_data.get('vacancy')
        user = vacancy.user
        notification = Notification.objects.create(
            user = user,
            message = f"{validated_data['applicant']} has sent an application for your {vacancy.job_title} job."
        )



        return job_application


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


