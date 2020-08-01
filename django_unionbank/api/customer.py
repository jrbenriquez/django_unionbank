import requests
import json
import logging
from urllib.parse import urlencode
from datetime import datetime
from rest_framework.exceptions import APIException
from django_unionbank.api.codes import PENDING_RESPONSE
from django_unionbank import settings as ub_settings
from django_unionbank.constants import TRANSACTION_FEES
from django_unionbank.models import FundTransfer
from django_unionbank.utils import generate_ft_reference_id
from django_unionbank.api.partner_authentication import get_partner_token

error_logger = logging.getLogger('pahiram')
logger = logging.getLogger('unionbank')


def customer_authentication():
    PRODUCT_NAME = 'UnionBank Customer Authentication 2.0.0'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/customers/v1/oauth2/authorize'
    )

    response_type = 'code'
    client_id = ub_settings.UNIONBANK_CLIENT_ID
    redirect_uri = 'http://localhost:8000/oauth_callback/ubp/'
    _type = 'single'
    scope = 'transfers instapay pesonet transfers_pesonet account_inquiry account_info'
    partner_id = ub_settings.UNIONBANK_PARTNER_ID


    params = {
        "response_type": response_type,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "type": _type,
        'scope': scope,
        "partner_id": partner_id
    }
    return f"{ENDPOINT_URL}?{urlencode(params)}"


def customer_code_for_token(data):
    PRODUCT_NAME = 'Request Online Access Token'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/customers/v1/oauth2/token'
    )

    headers = {
        "Content-Type": 'application/x-www-form-urlencoded',
        "x-ibm-client-id": ub_settings.UNIONBANK_CLIENT_ID,
        "x-ibm-client-secret": ub_settings.UNIONBANK_CLIENT_SECRET
    }

    data['client_id'] = ub_settings.UNIONBANK_CLIENT_ID
    data['redirect_uri'] = 'http://localhost:8000/oauth_callback/ubp/'

    response = requests.post(ENDPOINT_URL, data=data, headers=headers)
    response_data = json.loads(response.text)

    if response.status_code == 200:
        return response_data
    return response_data


def customer_fund_transfer(access_token, reference_id, account_number, amount,
                           remarks=None, particulars=None, recipient_name=None, message=None):
    PRODUCT_NAME = 'Request Online Access Token'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/online/v2/transfers/single'
    )

    request_date = datetime.now().isoformat()[:-3]
    info = []
    if not remarks:
        remarks = "No Remarks"
    if not particulars:
        particulars = "No Particulars"
    if recipient_name:
        recipient_dict = {
          "index": 1,
          "name": "Recipient",
          "value": f"{recipient_name}"
        }
        info.append(recipient_dict)
    if message:
        message_dict = {
          "index": 2,
          "name": "Message",
          "value": f"{message}"
        }
        info.append(message_dict)

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-ibm-client-id": ub_settings.UNIONBANK_CLIENT_ID,
        "x-ibm-client-secret": ub_settings.UNIONBANK_CLIENT_SECRET,
        "authorization": f"Bearer {access_token}",
        "x-partner-id": ub_settings.UNIONBANK_PARTNER_ID
    }

    data = {
      "senderRefId": reference_id,
      "tranRequestDate": request_date,
      "accountNo": account_number,
      "amount": {
        "currency": "PHP",
        "value": f"{amount}"
      },
      "remarks": remarks,
      "particulars": particulars,
      "info": info
    }

    response = requests.post(ENDPOINT_URL, data=data, headers=headers)
    response_data = json.loads(response.text)
    return response_data





