# -*- coding: utf-8 -*-
import requests
import json
import hashlib

from django.utils.translation import ugettext_lazy as _
from .config import MailChimpConfig


config = MailChimpConfig()


def check_response_status(response):
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(_(u'Error: {} {}').format(str(response.status_code), err))
    except ValueError:
        raise ValueError(_(u'Cannot decode json, got {}').format(response.text))


def get_hash_md5(email):
    hashlib.md5(email.encode('utf-8')).hexdigest()

def get_status_if_new():
    """
    You should pass the value “subscribed” in the API field instead of “pending”. Using “pending” will
    always send a double opt-in confirmation until that users confirms their subscription.
    By passing “subscribed” you will bypass this method.
    """
    return 'pending' if config.double_optin else 'subscribed'

def subscribe_member_to_list(data, list_id=config.default_list_id):

    member_hash = get_hash_md5(data['email_address'])
    data = json.dumps(data)

    # PUT new or modify existing member
    response = requests.put(
        config.api_root + 'lists/{}/members/{}'.format(list_id, member_hash),
        auth=('apikey', config.apikey),
        data=data
    )

    check_response_status(response)

