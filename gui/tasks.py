from celery import shared_task
from django.utils import timezone

from gui.email import send_subscription_emails

@shared_task
def subscription_email_task():
    send_subscription_emails(timezone.now())