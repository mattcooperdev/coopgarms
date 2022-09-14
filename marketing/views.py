from django.shortcuts import render
from django.contrib import messages

from django.conf import settings

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError


# Code taken from
# https://mailchimp.com/developer/marketing/guides/create-your-first-audience/


# Mailchimp Keys
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


def subscription(request):
    '''Newsletter subscription'''
    template = 'marketing/index.html'
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        messages.success(request, "Subscription received. Thank You! ")
    return render(request, template)


# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
        "server": server
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }
    try:
        response = client.lists.add_list_member(list_id, member_info)
        print(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))

