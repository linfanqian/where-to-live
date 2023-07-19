from datetime import timedelta

from django.core.mail import send_mass_mail

from .models import Subscription
from .enums import Platform
from .mapping import search_condition_to_dict

from crawler.crawler import Crawler51

def send_subscription_emails(time):
    email_messages = []

    # Query subscriptions that need to send email at time
    subscriptions = Subscription.objects.filter(next_time=time)

    # Form email messages
    for subscription in subscriptions:
        search_result_list = []
        search_condition = subscription.search_condition
        if Platform.HOUSE51 in search_condition.platforms:
            house51_house_list = Crawler51().get_house_list(search_condition_to_dict(search_condition))
            search_result_list += house51_house_list

        search_result_str = "\n".join(search_result_list)
        message = (
            "Housing Search Results",
            search_result_str,
            "wheretolive@no-reply.com",
            [subscription.email]
        )

        email_messages.append(message)

        # Update time to send next email
        subscription.next_time += timedelta(hours=subscription.interval)
        subscription.save()

    # Send emails
    send_mass_mail(tuple(email_messages))