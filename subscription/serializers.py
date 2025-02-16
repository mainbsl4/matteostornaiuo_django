from rest_framework import serializers

from .models import Packages, Subscription


class PackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = '__all__'
        