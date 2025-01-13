from .models import User, Skill
from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ("id", "email", "first_name", "last_name", "password")
        fields = ("id", "email", "first_name", "last_name", "is_client", "is_staff", "date_joined")
        extra_kwargs = {
            'email': {'required': False}  # Mark email as not required
        }
        # fields = "__all__"

class StaffSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email","first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if validate_password(validated_data["password"]) == None:
            password = make_password(validated_data["password"])
            user = User.objects.create(
                # username=validated_data["username"],
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                password=password,
                is_staff=True
            )
        return user
    

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ClientSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if validate_password(validated_data["password"]) == None:
            password = make_password(validated_data["password"])
            user = User.objects.create(
                # username=validated_data["username"],
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                password=password,
                is_client=True
            )
        return user
