from celery import shared_task
from django.utils import timezone
from .models import Vacancy

@shared_task
def update_job_status():
    now = timezone.now()
    print('i am called')
    # Update jobs to "IN_PROGRESS" if their start time has passed
    Vacancy.objects.filter(start_date__lte=now.date(), start_time__lte=now.time(), status='active').update(status='progress')

    # Update Vacancys to "FINISHED" if their end time has passed
    Vacancy.objects.filter(end_date__lte=now.date(), end_time__lte=now.time(), status='progress').update(status='finished')


@shared_task
def print_hello():
    print('Hello world')