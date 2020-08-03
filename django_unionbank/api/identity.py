import requests
import json
import logging
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


def get_last_running_balance():
    PRODUCT_NAME = 'Partner Unionbank-to-UnionBank Fund Transfer'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/portal/accounts/v1/transactions'
    )
    token = get_partner_token('account_inquiry')
    partner_id = ub_settings.UNIONBANK_PARTNER_ID

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-ibm-client-id': ub_settings.UNIONBANK_CLIENT_ID,
        'x-ibm-client-secret': ub_settings.UNIONBANK_CLIENT_SECRET,
        'authorization': 'Bearer {}'.format(token),
        'x-partner-id': partner_id
    }

    response = requests.get(ENDPOINT_URL, headers=headers)
    if not response.text:
        logger.error('[{}] Unexpected No Response'.format(response.status_code))
        raise APIException(code='400', detail='Unexpected No Response')
    response_data = json.loads(response.text)
    if 'records' in response_data:
        records = response_data['records']
    else:
        records = None

    if 'totalRecords' in response_data:
        record_count = response_data['totalRecords']
    else:
        raise APIException(code='400', detail='Unexpected No Record Count in Response')

    if 'lastRunningBalance' in response_data:
        balance = response_data['lastRunningBalance']
    else:
        raise APIException(code='400', detail='Unexpected No Balance Response')

    return balance, records, record_count


def partner_funds_transfer(token, account_number,
                           amount, remarks=None, particulars=None,
                           info=None, reference_id=None, currency="PHP"):
    PRODUCT_NAME = 'Partner Unionbank-to-UnionBank Fund Transfer'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/partners/v3/transfers/single'
    )
    result = None
    if not reference_id:
        reference_id = generate_ft_reference_id(method='ubp')

    requested_at = datetime.now().isoformat()[:-3]

    partner_id = ub_settings.UNIONBANK_PARTNER_ID

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-ibm-client-id': ub_settings.UNIONBANK_CLIENT_ID,
        'x-ibm-client-secret': ub_settings.UNIONBANK_CLIENT_SECRET,
        'authorization': 'Bearer {}'.format(token),
        'x-partner-id': partner_id
    }
    if not remarks:
        remarks = ''
    if not particulars:
        particulars = ''
    data = {
        "senderRefId": reference_id,
        "tranRequestDate": requested_at,
        "accountNo": account_number,
        "amount": {
            "currency": currency,
            "value": amount
        },
        "remarks": remarks,
        "particulars": particulars,
        "info": info
    }

    if info:
        data["info"] = info

    logger.info(data)
    response = requests.post(ENDPOINT_URL, json=data, headers=headers)
    if not response.text:
        logger.error('[{}] Unexpected No Response'.format(response.status_code))
        raise APIException(code='400', detail='Unexpected No Response')
    response_data = json.loads(response.text)

    if response_data.get('httpCode', None) == '401' and \
        response_data.get('httpMessage', None) == 'Unauthorized' and \
            response_data.get('moreInformation', None) == 'Not registered to plan':

        raise APIException('Not Registered to required plan for {}'.format(PRODUCT_NAME),
                           code=response_data.get('httpCode', None))

    # TODO Create fund transfer
    if response.status_code not in [requests.codes.created, requests.codes.ok]:
        try:
            logger.error("{}".format(response_data))
            main_error = response_data['errors'][0]
            response_code = main_error['code']
            response_description = main_error['description']
            message = "[CODE-{}] {}".format(response_code, response_description)
            logger.error("{} - {}".format(message, data))
            raise APIException(message,
                               code=response.status_code)
        except KeyError as e:
            error_logger.error(e)
            raise APIException("Unknown Error. Please check logs. Unionbank Payout might have to be repeated",
                               code=requests.codes.server_error)

    transfer = FundTransfer.objects.create(
        reference_id=reference_id,
        transaction_id=response_data['ubpTranId'],
        requested_at=requested_at,
        beneficiary=account_number,
        sender_partner_id=partner_id,
        remarks=remarks,
        amount=amount,
        currency=currency,
        status=FundTransfer.SUCCESS,
        channel=FundTransfer.FUNDTRANSFER,
        fee=0
    )

    return transfer, result

