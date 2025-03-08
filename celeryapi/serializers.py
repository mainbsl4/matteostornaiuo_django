from rest_framework import serializers
from staff.models import Staff


class StaffInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    swift_code = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Staff
        fields = ['id','full_name', 'email', 'phone', 'nid_number', 'dob', 'swift_code']

    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    def get_email(self, obj):
        return obj.user.email
    def get_swift_code(self, obj):
        return f'{obj.bankdetails.swift_code}'
    