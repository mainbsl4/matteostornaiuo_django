from rest_framework import serializers

from users.serializers import SkillSerializer
from users.models import Skill

from django.contrib.auth import get_user_model

from .models import (
    CompanyProfile,
    JobTemplate,
    Job,
    Vacancy,



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
    
    class Meta:
        model = Vacancy
        fields = '__all__'

    def create(self, validated_data):
        skill_data = validated_data.pop('skills', {})
        user = validated_data.pop('user')
        # user = User.objects.get(pk=user_data)
        vacancy = Vacancy.objects.create(user=user,**validated_data)
        for skill in skill_data:
            skill,_ = Skill.objects.get_or_create(**skill)
            vacancy.skills.add(skill)
        return vacancy
    

class JobSerializer(serializers.ModelSerializer):
    vacancy = VacancySerializer(many=True)
    class Meta:
        model = Job
        fields = '__all__'

    def create(self, validated_data):
        vacancy_data = validated_data.pop('vacancy')
        
        print('vcancy data:', vacancy_data)
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

        return job

