from rest_framework import serializers



from .models import (
    CompanyProfile,
    JobTemplate,
    Job,


)


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'
        read_only_fields = ['user']


class JobTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTemplate
        fields = '__all__'
        read_only_fields = ['user']

# jbo serializers 
# {
#         "id": 1,
#         "job_template": {
#             "id": 4,
#             "job_title": "Cleaner",
#             "number_of_staff": 1,
#             "uniform": "White Shirt, Black Pank, Black Shoes",
#             "open_date": "2025-01-08",
#             "close_date": "2025-01-09",
#             "start_time": "11:47:26",
#             "end_time": "18:00:00",
#             "created_at": "2025-01-08T12:25:43.369695Z",
#             "updated_at": "2025-01-08T12:25:43.369712Z",
#             "user": 1,
#             "skills": [
#                 1
#             ]
#         },
#         "company": {
#             "id": 3,
#             "company_name": "ABC Company Updated",
#             "contact_number": "982472",
#             "company_email": "example@gmail.com",
#             "billing_email": "billing@example.com",
#             "company_address": "Gulshan",
#             "company_details": "Example company details",
#             "company_logo": null,
#             "created_at": "2025-01-08T11:37:07.290490Z",
#             "updated_at": "2025-01-08T11:37:07.290510Z",
#             "user": 1
#         },
#         "title": "Need some cleaner",
#         "description": "Hi example desc.",
#         "created_at": "2025-01-08T12:29:17.711670Z",
#         "updated_at": "2025-01-08T12:29:17.711691Z"
#     }
class JobSerializer(serializers.ModelSerializer):
    job_template = serializers.PrimaryKeyRelatedField(queryset=CompanyProfile.objects.all())
    company = serializers.PrimaryKeyRelatedField(queryset= JobTemplate.objects.all())
    class Meta:
        model = Job
        fields = '__all__'

    # add job_template and company with that job model
    
