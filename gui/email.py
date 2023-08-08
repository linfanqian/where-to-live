from datetime import timedelta

from django.core.mail import send_mail, send_mass_mail

from .models import Subscription
from .enums import Platform
from .mapping import search_condition_to_dict

from website.settings import DEFAULT_FROM_EMAIL

from crawler.crawler import Crawler51

def send_thank_email(receiver, start_time, end_time, interval):
    message = f"Thank you for subscribing.\n" + \
              f"You will receive notification emails about rentals with which " + \
              f"conditions you selected from {start_time} to {end_time} " + \
              f"for each {interval} hours."

    send_mail(
        "Subscription Confirmation",
        message,
        DEFAULT_FROM_EMAIL,
        [receiver,]
    )

def send_subscription_emails(time):
    email_messages = []

    # Query subscriptions that need to send email at time
    subscriptions = Subscription.objects.filter(next_time__lte=time)

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
            DEFAULT_FROM_EMAIL,
            [subscription.email]
        )

        email_messages.append(message)

        # Update time to send next email
        subscription.next_time += timedelta(hours=subscription.interval)
        subscription.save()

    # Send emails
    send_mass_mail(tuple(email_messages))