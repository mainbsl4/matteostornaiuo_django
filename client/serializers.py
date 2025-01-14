from rest_framework import serializers

from users.serializers import SkillSerializer, JobRoleSerializer, UniformSerializer
from users.models import Skill

from django.contrib.auth import get_user_model

from .models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy,



)
from users.models import (
    JobRole,
    Skill,
    Uniform,

)

User = get_user_model()

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'
        read_only_fields = ['user']


class JobTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTemplate
        fields = '__all__'
        # read_only_fields = ['profile']
class VacancySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    job_title = JobRoleSerializer()
    uniform = UniformSerializer()
    class Meta:
        model = Vacancy
        fields = '__all__'

    def create(self, validated_data):
        print('validated data:', validated_data)
        skill_data = validated_data.pop('skills', {})
        user = validated_data.pop('user')
        job_title_data = validated_data.pop('job_title')
        uniform_data = validated_data.pop('uniform')
        
        job_title = job_title_data['name']
        uniform = uniform_data['name']

        job_role = JobRole.objects.filter(name__iexact=job_title).first()
        uniform = Uniform.objects.filter(name__iexact=uniform).first()
        # user = User.objects.get(pk=user_data)
        vacancy = Vacancy.objects.create(user=user,job_title=job_role,uniform=uniform,**validated_data)
        for skill in skill_data:
            skill,_ = Skill.objects.get_or_create(**skill)
            vacancy.skills.add(skill)
        return vacancy
    # def update(self, instance, validated_data):

    

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
    

