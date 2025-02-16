from rest_framework import serializers 

from .models import  CompanyReview, Notification
from staff.serializers import StaffSerializer
from client.models import Vacancy
from client.serializers import JobViewSerializers, VacancySerializer
from users.models import Skill



class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        exclude = ('created_at',)
        read_only_fields = ['staff', 'profile', 'vacancy']
        # depth = 2

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class VacancyJobSerializer(serializers.Serializer):
    job = JobViewSerializers()
    vacancy = VacancySerializer()
    
