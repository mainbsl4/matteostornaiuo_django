import datetime
from django.core.management.base import BaseCommand
from client.models import JobApplication, Vacancy  

class Command(BaseCommand):
    help = 'Update job applications to expired if their vacancy close date has passed'

    def handle(self, *args, **kwargs):
        today = datetime.date.today()

        # Find expired vacancies
        expired_vacancies = Vacancy.objects.filter(close_date__lt=today)

        # Update job applications linked to those vacancies (except accepted jobs)
        updated_count = JobApplication.objects.filter(
            vacancy__in=expired_vacancies
        ).exclude(job_status='accepted').update(job_status='expired')

        self.stdout.write(f'Successfully updated {updated_count} expired job applications.')
