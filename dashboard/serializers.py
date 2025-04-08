from rest_framework import serializers 

from .models import Notification,TermsAndConditions,Report
from staff.serializers import StaffSerializer
from client.models import Vacancy
from client.serializers import JobViewSerializers, VacancySerializer
from users.models import Skill



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
    

class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        exclude = ('created_at',)
    
class ReportSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Report
        fields = '__all__'