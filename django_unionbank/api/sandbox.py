import requests
import json
import logging
from urllib.parse import urlencode
from datetime import datetime
from rest_framework.exceptions import APIException
from django_unionbank.api.codes import PENDING_RESPONSE
from django_unionbank import settings as ub_settings
from django_unionbank.constants import TRANSACTION_FEES
from django_unionbank.models import SandBoxAccount
from django_unionbank.utils import generate_ft_reference_id
from django_unionbank.api.partner_authentication import get_partner_token

error_logger = logging.getLogger('pahiram')
logger = logging.getLogger('unionbank')


def create_sandbox_account(username, password, account_name):
    PRODUCT_NAME = 'Create Sandbox Account'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/sandbox/v1/accounts'
    )

    headers = {
        "accept": 'application/json',
        "content-type": 'application/json',
        "x-ibm-client-id": ub_settings.UNIONBANK_CLIENT_ID,
        "x-ibm-client-secret": ub_settings.UNIONBANK_CLIENT_SECRET
    }

    data = {
        "username": username,
        "password": password,
        "account_name": account_name
    }

    response = requests.post(ENDPOINT_URL, json=data, headers=headers)
    response_data = json.loads(response.text)
    print(ENDPOINT_URL)
    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        account_data = response_data['data']['account']
        username = response_data['data']['user']['username']
        password = response_data['data']['user']['password']

        sb_account = SandBoxAccount.objects.create(username=username, password=password, **account_data)
        return sb_account
    else:
        return False






