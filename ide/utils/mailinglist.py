import logging
import mailchimp

from django.conf import settings


mailchimp_api = mailchimp.Mailchimp(apikey=settings.MAILCHIMP_API_KEY)
mailchimp_default_list_id = settings.MAILCHIMP_LIST_ID


def add_user(user, mailing_list_id=None):
    if mailchimp_api is None:
        logging.error("Missing MAILCHIMP_API_KEY environment variable")

    list_id = mailing_list_id or mailchimp_default_list_id
    if list_id is None:
        logging.error("Missing MAILCHIMP_LIST_ID environment variable")

    try:
        response = mailchimp_api.lists.subscribe(list_id,
                                                 {'email': user.email},
                                                 double_optin=False,
                                                 update_existing=False,
                                                 replace_interests=False)
        logging.debug("{} was successfully subscribed to list {}".format(response['email'], list_id))
    except mailchimp.ListDoesNotExistError:
        logging.error("List {} does not exist".format(list_id))
    except mailchimp.ListAlreadySubscribedError:
        logging.info("User already subscribed to list {}".format(list_id))
    except mailchimp.Error as e:
        logging.error("An error occurred: {} - {}".format(e.__class__, e))
