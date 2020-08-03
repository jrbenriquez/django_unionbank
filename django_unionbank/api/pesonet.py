import requests
import json
import logging
from datetime import datetime
from rest_framework.exceptions import APIException, ValidationError

from django_unionbank.api.codes import PENDING_RESPONSE
from django_unionbank import settings as ub_settings
from django_unionbank.models import FundTransfer, PESONetBank
from django_unionbank.constants import TRANSACTION_FEES
from django_unionbank.utils import generate_ft_reference_id
from django_unionbank.api.identity import get_partner_token

error_logger = logging.getLogger('pahiram')
logger = logging.getLogger('unionbank')

def update_pesonet_banks():
    PRODUCT_NAME = 'Update PESONet Receiving Banks'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/partners/v3/pesonet/banks'
    )
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-ibm-client-id': ub_settings.UNIONBANK_CLIENT_ID,
        'x-ibm-client-secret': ub_settings.UNIONBANK_CLIENT_SECRET,
        'x-partner-id': ub_settings.UNIONBANK_PARTNER_ID
    }

    # Make request using credentials
    response = requests.get(ENDPOINT_URL, headers=headers)
    if not response.text:
        logger.error('[{}] Unexpected No Response'.format(response.status_code))
        raise APIException(code='400', detail='Unexpected No Response')
    response_data = json.loads(response.text)
    # Store received object list
    for bank in response_data['records']:
        # Check if bank already exists:
        bank_query = PESONetBank.objects.filter(code=bank['code'], name=bank['bank'])
        if not bank_query.exists():
            pso_bank = PESONetBank.objects.create(
                name=bank['bank'],
                code=bank['code'],
                brstn=bank['brstn']
            )
            logger.info("{} Created".format(pso_bank.name))
    logger.info('PESONet Receiving Banks List Updating Done!')
    return response['records']


def verify_single_pesonet_transaction(reference_id):
    PRODUCT_NAME = 'Check Single PESOnet Inter-Bank Funds Transfer via Partners status'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/partners/v3/pesonet/transfers/single/'
    )

    partner_id = ub_settings.UNIONBANK_PARTNER_ID

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-ibm-client-id': ub_settings.UNIONBANK_CLIENT_ID,
        'x-ibm-client-secret': ub_settings.UNIONBANK_CLIENT_SECRET,
        'x-partner-id': partner_id
    }

    logger.info('Checking PESONet status for {}'.format(reference_id))
    response = requests.get("{}{}".format(ENDPOINT_URL, reference_id), headers=headers)
    if not response.text:
        logger.error('[{}] Unexpected No Response'.format(response.status_code))
        raise APIException(code='400', detail='Unexpected No Response')
    response_data = json.loads(response.text)
    return response_data['record']


def test_only_update_transaction(reference_id, status):
    PRODUCT_NAME = 'Update Transaction'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/partners/v3/pesonet/transactions/update'
    )
    token = get_partner_token('transfers_pesonet')
    partner_id = ub_settings.UNIONBANK_PARTNER_ID

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-ibm-client-id': ub_settings.UNIONBANK_CLIENT_ID,
        'x-ibm-client-secret': ub_settings.UNIONBANK_CLIENT_SECRET,
        'x-partner-id': partner_id,
        'authorization': 'Bearer {}'.format(token)
    }

    data = {
        "status": status,
        "remittanceId": reference_id
    }

    logger.info('Updating PESONet TEST status for {}'.format(reference_id))
    response = requests.post(ENDPOINT_URL, json=data, headers=headers)
    if not response.text:
        logger.error('[{}] Unexpected No Response'.format(response.status_code))
        raise APIException(code='400', detail='Unexpected No Response')
    response_data = json.loads(response.text)
    print(response_data)
    if response.status_code not in [requests.codes.created, requests.codes.ok]:
        raise APIException(code='400', detail='Unable to Update')

    return response_data


def partner_pesonet_fund_transfer(token, data,
                                   reference_id=None, currency='PHP'):
    PRODUCT_NAME = 'Partner PESONet Fund Transfer'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/partners/v3/pesonet/transfers/single'
    )

    if not reference_id:
        reference_id = generate_ft_reference_id(method='pesonet')
    requested_at = datetime.now().isoformat()[:-3]
    logger.info('Initiating PESONet Transfer')
    result = None
    remarks = None
    # Check validity of sender_data
    sender_name = data.get('sender_name')
    sender_address = data.get('sender_address')
    # Check validity of beneficiary_data
    beneficiary_account = data.get('beneficiary_account')
    beneficiary_name = data.get('beneficiary_name')
    beneficiary_address = data.get('beneficiary_address')

    # Check validity of remittance_data
    remittance_amount = data.get('remittance_amount')
    remittance_bank = data.get('remittance_bank')
    remittance_purpose = data.get('remittance_purpose')
    remittance_instructions = data.get('remittance_instructions')

    partner_id = ub_settings.UNIONBANK_PARTNER_ID

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-ibm-client-id': ub_settings.UNIONBANK_CLIENT_ID,
        'x-ibm-client-secret': ub_settings.UNIONBANK_CLIENT_SECRET,
        'authorization': 'Bearer {}'.format(token),
        'x-partner-id': partner_id
    }

    data = {
        'senderRefId': reference_id,
        "tranRequestDate": requested_at,
        "sender": {
            "name": sender_name,
            "address": sender_address
        },
        "beneficiary": {
            "accountNumber": beneficiary_account,
            "name": beneficiary_name,
            "address": beneficiary_address
        },
        "remittance": {
            "amount": "{0:.2f}".format(remittance_amount),
            "currency": currency,
            "receivingBank": remittance_bank,
            "purpose": remittance_purpose,
            "instructions": remittance_instructions
        }
    }
    logger.info(data)
    response = requests.post(ENDPOINT_URL, json=data, headers=headers)
    if not response.text:
        logger.error('[{}] Unexpected No Response'.format(response.status_code))
        raise APIException(code='400', detail='Unexpected No Response')
    response_data = json.loads(response.text)
    logger.info("[{}] {}".format(response.status_code, response_data))
    if response_data.get('httpCode', None) == '401' and \
        response_data.get('httpMessage', None) == 'Unauthorized' and \
        response_data.get('moreInformation', None) == 'Not registered to plan':
        raise APIException('Not Registered to required plan for {}'.format(PRODUCT_NAME),
                           code=response_data.get('httpCode', None))
    logger.info('Response')
    logger.info("[{}] {}".format(response.status_code, response.text))
    # TODO create Fund Transfer Model
    if response.status_code not in [requests.codes.created, requests.codes.ok]:
        try:
            main_error = response_data['errors'][0]
            response_code = main_error['code']
            response_description = main_error['description']
            message = "[CODE-{}] {}".format(response_code, response_description)
            logger.error("{} - {}".format(message, data))

            raise ValidationError(message)
        except KeyError as e:
            logger.error(e)
            raise ValidationError("Unknown Error. Please check logs. Unionbank Payout might have to be repeated")
    status = FundTransfer.PENDING

    logger.info(response_data)
    transfer = FundTransfer.objects.create(
        reference_id=reference_id,
        transaction_id=response_data['ubpTranId'],
        requested_at=requested_at,
        beneficiary=beneficiary_account,
        sender_partner_id=partner_id,
        remarks=remarks,
        amount=remittance_amount,
        currency=currency,
        status=status,
        channel=FundTransfer.PESONET,
        fee=TRANSACTION_FEES.get('pesonet', 25)
    )

    return transfer, result