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

from dashboard.models import FavouriteStaff

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
    skills = SkillSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    job_title = JobRoleSerializer()
    uniform = UniformSerializer()
    jobs = JobSerializerForVacancy(many=True, read_only=True, source='vacancies')

    # add alist of staff id for sending invitation this field is write only
    staff_ids = serializers.ListField(write_only=True)


    class Meta:
        model = Vacancy
        # add staff_ids with fields 

        fields = ['user', 'job_title','number_of_staff', 'skills', 'uniform','open_date','close_date', 'start_time', 'end_time','salary', 'participants', 'staff_ids','jobs']

    def create(self, validated_data):
        print('validated data:', validated_data)
        skill_data = validated_data.pop('skills', {})
        user = validated_data.pop('user')
        job_title_data = validated_data.pop('job_title')
        uniform_data = validated_data.pop('uniform')
        
        staff_ids = validated_data.pop('staff_ids', [])
        print('staff_ids:', staff_ids)
        
        job_title = job_title_data['name']
        uniform = uniform_data['name']

        job_role = JobRole.objects.filter(name__iexact=job_title).first()
        uniform = Uniform.objects.filter(name__iexact=uniform).first()
        # user = User.objects.get(pk=user_data)
        vacancy = Vacancy.objects.create(user=user,job_title=job_role,uniform=uniform,**validated_data)
        for skill in skill_data:
            skill,_ = Skill.objects.get_or_create(**skill)
            vacancy.skills.add(skill)
        
        # send invitation 
        for staff_id in staff_ids:
            staff_ = get_object_or_404(FavouriteStaff, pk=staff_id)
            staff = Staff.objects.filter(id=staff_.staff.id).first()
            if not staff:
                continue
            invitation = StaffInvitation.objects.create(vacancy=vacancy, staff=staff)
            invitation.save()

        return vacancy
    # def update(self, instance, validated_data):


class CreateVacancySerializers(serializers.ModelSerializer):
    job_title = serializers.PrimaryKeyRelatedField(queryset=JobRole.objects.all())
    skills_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    uniform = serializers.PrimaryKeyRelatedField(queryset=Uniform.objects.all())
    # participants = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = Vacancy
        fields = ['user', 'job_title','number_of_staff','skills_id','uniform', 'open_date', 'close_date', 'start_time', 'end_time']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        print('validated data', validated_data)

        user = self.context['request'].user
        validated_data['user'] = user

        job_title = validated_data.pop('job_title')
        print('job_title', job_title)
        skills = validated_data.pop('skills')
        print('skills', skills)
        uniform = validated_data.pop('uniform')
        print('uniform', uniform)
        participants = validated_data.pop('participants')
        print('participants', participants)

        vacancy = Vacancy.objects.create(
            job_title=job_title,
            uniform=uniform,
            participants=participants,
            **validated_data
        )
        vacancy.skills.set(skills)
        return vacancy



        # print all this
        return 0

class JobSerializer(serializers.ModelSerializer):
    vacancy = VacancySerializer(many=True)
    class Meta:
        model = Job
        fields = '__all__'



    def create(self, validated_data):
        vacancy_data = validated_data.pop('vacancy')
        user_ = vacancy_data[0].get('user')
        save_in_template = validated_data.get('save_template', False)
        
        job = Job.objects.create(**validated_data)
        for vacancy in vacancy_data:
            vacancy['user'] = vacancy['user'].id
            vacancy_serializer = VacancySerializer(data=vacancy)
            if vacancy_serializer.is_valid():
                vacancy_serializer.save()
                vacancy_instance = vacancy_serializer.instance
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
    def update(self, instance, validated_data):
        # Update Job instance attributes
        vacancy_data = validated_data.pop('vacancy', [])
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        # Extract the vacancy data from validated_data

        # Create a list to hold the updated vacancies
        updated_vacancies = []

        # Loop through the provided vacancy data
        for vacancy_info in vacancy_data:
            vacancy_id = vacancy_info.get('id', None)

            if 'user' in vacancy_info and isinstance(vacancy_info['user'], User): 
                vacancy_info['user'] = vacancy_info['user'].id

            if vacancy_id:
                # Update the existing vacancy
                try:
                    vacancy_instance = instance.vacancy.get(id=vacancy_id)
                    vacancy_serializer = VacancySerializer(vacancy_instance, data=vacancy_info)
                    if vacancy_serializer.is_valid():
                        vacancy_instance = vacancy_serializer.save()
                        updated_vacancies.append(vacancy_instance)  # Add to updated vacancies list
                    else:
                        print(f'Vacancy serializer is not valid for ID {vacancy_id}:', vacancy_serializer.errors)
                except Vacancy.DoesNotExist:
                    print(f'Vacancy with ID {vacancy_id} does not exist.')
            else:
                # Create a new vacancy if no ID is provided
                vacancy_serializer = VacancySerializer(data=vacancy_info)
                if vacancy_serializer.is_valid():
                    vacancy_instance = vacancy_serializer.save()
                    updated_vacancies.append(vacancy_instance)  # Add the new vacancy to the list
                else:
                    print('Vacancy serializer is not valid for new vacancy:', vacancy_serializer.errors)

        # Use set() to update the many-to-many relationship
        instance.vacancy.set(updated_vacancies)

        # Save the updated job instance
        instance.save()
        return instance
    


class JobApplicationSerializer(serializers.ModelSerializer):
    vacancy = serializers.PrimaryKeyRelatedField(queryset=Vacancy.objects.all())
    applicant = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all())

    class Meta:
        model = JobApplication
        fields = '__all__'
   
    def create(self, validated_data):
        print('validated data', validated_data)

        return 0
