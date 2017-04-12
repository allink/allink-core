# -*- coding: utf-8 -*-
import requests
import json
import hashlib
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from raven import Client
from allink_core.allink_mailchimp.config import MailChimpConfig


config = MailChimpConfig()


def check_response_status(response):
    client = Client(settings.RAVEN_CONFIG.get('dns'))
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        client.captureException()
        raise requests.exceptions.HTTPError(_(u'Error: {} {}').format(str(response.status_code), err))
    except ValueError as err:
        client.captureException()
        raise ValueError(_(u'Cannot decode json, got {}').format(response.text), err)


def get_hash_md5(email):
    return hashlib.md5(email.encode('utf-8')).hexdigest()


def get_status_if_new():
    """
    You should pass the value “subscribed” in the API field instead of “pending”. Using “pending” will
    always send a double opt-in confirmation until that users confirms their subscription.
    By passing “subscribed” you will bypass this method.
    """
    return 'pending' if config.double_optin else 'subscribed'


def list_members_post(data, list_id=config.default_list_id, member_hash_email=None):
    member_hash = get_hash_md5(member_hash_email) if member_hash_email else get_hash_md5(data['email_address'])
    data = json.dumps(data)
    # POST new member
    try:
        response = requests.post(
            config.api_root + 'lists/{}/members/{}'.format(list_id, member_hash),
            auth=('apikey', config.apikey),
            data=data
        )
        check_response_status(response)
    except:
        pass


def list_members_put(data, list_id=config.default_list_id, member_hash_email=None):
    member_hash = get_hash_md5(member_hash_email) if member_hash_email else get_hash_md5(data['email_address'])
    data = json.dumps(data)
    try:
        # PUT new or modify existing member
        response = requests.put(
            config.api_root + 'lists/{}/members/{}'.format(list_id, member_hash),
            auth=('apikey', config.apikey),
            data=data
        )
        check_response_status(response)
    except:
        pass


def list_members_patch(data, list_id=config.default_list_id, member_hash_email=None):
    member_hash = get_hash_md5(member_hash_email) if member_hash_email else get_hash_md5(data['email_address'])
    data = json.dumps(data)
    # PATCH existing member
    response = requests.patch(
        config.api_root + 'lists/{}/members/{}'.format(list_id, member_hash),
        auth=('apikey', config.apikey),
        data=data
    )
    check_response_status(response)


def list_members_delete(data, list_id=config.default_list_id, member_hash_email=None):
    member_hash = get_hash_md5(member_hash_email) if member_hash_email else get_hash_md5(data['email_address'])
    # DELETE existing member
    response = requests.delete(
        config.api_root + 'lists/{}/members/{}'.format(list_id, member_hash),
        auth=('apikey', config.apikey),
    )
