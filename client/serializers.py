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
    StaffInvitation,
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

# class JobSerializerForVacancy(serializers.ModelSerializer):
#     company = CompanyProfileSerializer(read_only=True)
#     class Meta:
#         model = Job
#         fields = '__all__'

class VacancySerializer(serializers.ModelSerializer):
    client = CompanyProfileSerializer(read_only=True)
    status_count = serializers.SerializerMethodField()
    class Meta:
        model = Vacancy
        fields = [
            'id', 'jobs','client', 'job_title', 'number_of_staff', 'skills', 'uniform',
            'open_date', 'close_date', 'start_time', 'end_time',
            'salary','location', 'participants', 'shift_job', 'checkin_status', 'checkout_status','status_count', 'created_at'
        ]
        depth = 1
        # fields = ['user', 'job_title','number_of_staff', 'skills', 'uniform','open_date','close_date', 'start_time', 'end_time','salary', 'participants', 'staff_ids','jobs']

    # show number of accepted, rejected, expired and canceled jobs
    def get_status_count(self, obj):
        accepted = JobApplication.objects.filter(vacancy=obj, job_status='accepted').count()
        rejected = JobApplication.objects.filter(vacancy=obj, job_status='rejected').count()
        pending  = JobApplication.objects.filter(vacancy=obj, job_status='pending').count()
        expired = JobApplication.objects.filter(vacancy=obj, job_status='expired').count()
        print('Job status', accepted, rejected, pending, expired)
        return {
            'accepted': accepted,
            'rejected': rejected,
            'expired': expired,
            'pending': pending
        }
        # extra_fields = {
        #     'status_count': get_status_count
        # }

    


class CreateVacancySerializers(serializers.ModelSerializer):
    job_title = serializers.PrimaryKeyRelatedField(queryset=JobRole.objects.all())
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, required=False)
    uniform = serializers.PrimaryKeyRelatedField(queryset=Uniform.objects.all(), required=False, allow_null=True)
    invited_staff = serializers.ListField(write_only=True, required=False)
    # participants = serializers.PrimaryKeyRelatedField(queryset=FavouriteStaff.objects.all(), many=True)

    class Meta:
        model = Vacancy
        fields = ['client', 'job_title','number_of_staff','skills','uniform', 'open_date', 'close_date', 'start_time', 'end_time','location', 'invited_staff']
        read_only_fields = ['client']
    
    def create(self, validated_data):
        user = self.context['request'].user
        client = CompanyProfile.objects.get(user=user)
        validated_data['client'] = client

        # job_title = validated_data.get('job_title')
        skills = validated_data.pop('skills',[])

        invited_staff_ids = validated_data.pop('invited_staff', [])
        # print('invited_staff_ids:', invited_staff_ids)

        vacancy = Vacancy.objects.create(
            **validated_data
        )
        vacancy.skills.set(skills)

        if len(invited_staff_ids):
            for invited in invited_staff_ids:
                fav_staff = FavouriteStaff.objects.filter(id=invited).first()
                # print('invited staff', fav_staff)
                StaffInvitation.objects.create(vacancy=vacancy,staff=fav_staff.staff)
                # send notification
                notification = Notification.objects.create(
                    user = user,
                    message = f"{user.companyprofile.company_name} has invited you to a {vacancy.job_title.name} job application."
                )
        # send notification to all staff that match with the job_role
        # staff_with_similar_role = StaffRole.objects.filter(role=job_title)
        # for staff_role in staff_with_similar_role:
        #     staff = staff_role.staff
        #     notification = Notification.objects.create(
        #         user = staff.user,
        #         message = f"{user.companyprofile.company_name} has posted a new job for '{job_title}'."
        #     )
        
        return vacancy
    
    # update as similar create function
    def update(self, instance, validated_data):
        user = self.context['request'].user
        client = CompanyProfile.objects.get(user=user)
        validated_data['client'] = client
        
        job_title = validated_data.get('job_title')
        skills = validated_data.pop('skills')
        invited_staff_ids = validated_data.pop('invited_staff', [])

        vacancy = Vacancy.objects.get(pk=instance.pk)
        # Update the instance with validated data
        for attr, value in validated_data.items():
            setattr(vacancy, attr, value)
        
        vacancy.save()
        vacancy.skills.set(skills)
        
        for invited in invited_staff_ids:
            fav_staff = FavouriteStaff.objects.filter(id=invited).first()
            print('invited staff', fav_staff)
            StaffInvitation.objects.create(vacancy=instance, staff=fav_staff.staff)
            # send notification
            notification = Notification.objects.create(
                user = user,
                message = f"{user.companyprofile.company_name} has invited you to a {instance.job_title} job application."
            )
            # send notification to all staff that match with the job_role
            # staff_with_similar_role = StaffRole.objects.filter(role=job_title)
            # for staff_role in staff_with_similar_role:
            #     staff = staff_role.staff
            #     notification = Notification.objects.create(
            #         user = staff.user,
            #         message = f"{user.companyprofile.company_name} has posted a new job for '{job_title}'."
            #     )
        
        return vacancy
    

class JobSerializer(serializers.ModelSerializer):
    vacancies = serializers.ListField(
        write_only=True  # Use only for write operations
    )
    # company = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Job
        fields = ['id','company' , 'title', 'description', 'status', 'save_template', 'vacancies']
        read_only_fields = ['company']
        depth = 1    
    # to represantation for showing all the vacancy serializers data
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add the vacancy serializers data to the data
        data['vacancy'] = VacancySerializer(instance.vacancy, many=True).data
        # data['company'] = CompanyProfileSerializer(instance.company, read_only=True).data
        return data


    def create(self, validated_data):
        user_ = self.context['request'].user
        # user must be is client
        if not user_.is_client:
            return None
        client = CompanyProfile.objects.filter(user=user_).first()
        validated_data['company'] = client

        vacancy_data = validated_data.pop('vacancies')
        save_in_template = validated_data.get('save_template')
        
        job = Job.objects.create(**validated_data)
        # job_vacancies = []
        # for vacancy in vacancy_data:
        #     vacancy_serializer = CreateVacancySerializers(data=vacancy, context=self.context)
        #     if vacancy_serializer.is_valid():
        #         vacancy_obj = vacancy_serializer.save()
        #         job.vacancy.add(vacancy_obj)
        job.vacancy.set(vacancy_data)
        
        if save_in_template:
            job_template = JobTemplate.objects.create(client=user_.profiles, job=job)

        return job
    def update(self, instance, validated_data):
        user_ = self.context['request'].user
        # job = Job.objects.get(pk=instance.pk)
        # user must be is client
        if not user_.is_client:
            return None
        client = CompanyProfile.objects.filter(user=user_).first()
        validated_data['company'] = client

        vacancy_data = validated_data.pop('vacancies')
        save_in_template = validated_data.get('save_template',False)
        print('save in template: ', save_in_template)

        # update job objects 
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save_template = save_in_template
        instance.save()

        instance.vacancy.clear()
        instance.vacancy.set(vacancy_data)
        # for vacancy in instance.vacancy.all():
        #     vacancy.delete()

        # for vacancy in vacancy_data:
        #     vacancy_serializer = CreateVacancySerializers(data=vacancy, context=self.context)
        #     if vacancy_serializer.is_valid():
        #         vacancy_obj = vacancy_serializer.save()
        #         instance.vacancy.add(vacancy_obj)

        
        
        #job template have user and job field with foreign key relation
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
