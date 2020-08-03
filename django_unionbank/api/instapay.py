import requests
import json
import logging
from datetime import datetime
from rest_framework.exceptions import APIException, ValidationError

from django_unionbank.api.codes import PENDING_RESPONSE
from django_unionbank import settings as ub_settings
from django_unionbank.models import FundTransfer, InstapayBank
from django_unionbank.constants import TRANSACTION_FEES
from django_unionbank.utils import generate_ft_reference_id

error_logger = logging.getLogger('pahiram')
logger = logging.getLogger('unionbank')


def update_instapay_banks():
    PRODUCT_NAME = 'Update Instapay Receiving Banks'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/partners/v3/instapay/banks'
    )
    print(ENDPOINT_URL)
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
    if response.status_code != 200:
        raise Exception(f'[{response.status_code}] {response.text}')
    for bank in response_data['records']:
        # Check if bank already exists:
        bank_query = InstapayBank.objects.filter(code=bank['code'], name=bank['bank'])
        if not bank_query.exists():
            ipy_bank = InstapayBank.objects.create(
                name=bank['bank'],
                code=bank['code'],
                brstn=bank['brstn']
            )
            logger.info("{} Created".format(ipy_bank.name))
    logger.info('Instapay Receiving Banks List Updating Done!')
    return response['records']


def verify_single_instapay_transaction(reference_id):
    PRODUCT_NAME = 'Check Instapay Inter-Bank Funds Transfer via Partner status'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/partners/v3/instapay/transfers/single/'
    )

    partner_id = ub_settings.UNIONBANK_PARTNER_ID

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-ibm-client-id': ub_settings.UNIONBANK_CLIENT_ID,
        'x-ibm-client-secret': ub_settings.UNIONBANK_CLIENT_SECRET,
        'x-partner-id': partner_id
    }

    logger.info('Checking Instapay status for {}'.format(reference_id))
    response = requests.get("{}{}".format(ENDPOINT_URL, reference_id), headers=headers)
    if not response.text:
        logger.error('[{}] Unexpected No Response'.format(response.status_code))
        raise APIException(code='400', detail='Unexpected No Response')
    response_data = json.loads(response.text)
    return response_data['record']

def partner_instapay_fund_transfer(token, data,
                                   reference_id=None, currency='PHP'):
    PRODUCT_NAME = 'Partner Instapay Fund Transfer'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/partners/v3/instapay/transfers/single'
    )

    if not reference_id:
        reference_id = generate_ft_reference_id(method='instapay')
    requested_at = datetime.now().isoformat()[:-3]
    logger.info('Initiating Instapay Transfer')
    result = None
    remarks = None
    # Check validity of sender_data
    sender_name = data.get('sender_name')
    sender_addres = data.get('sender_address')
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
            "address": sender_addres
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
            remarks = response_description
            message = "[CODE-{}] {}".format(response_code, response_description)
            error_logger.error("{} - {}".format(message, data))
            logger.error("{} - {}".format(message, data))

            if response_code not in ['SP', 'SC']:
                raise ValidationError(message)

            response_code = response_code
        except KeyError as e:
            error_logger.error(e)
            raise ValidationError("Unknown Error. Please check logs. Unionbank Payout might have to be repeated")
    else:
        response_code = response_data['code']
    status = FundTransfer.PENDING
    if 'code' in response_data:
        if response_data['code'] == 'TS':
            status = FundTransfer.SUCCESS

    if response_code in ['SP', 'SC']:
        main_error = response_data['errors'][0]
        details = main_error['details']
        transaction_id = details['ubpTranId']

    else:
        transaction_id = response_data['ubpTranId']

    logger.info(response_data)
    transfer = FundTransfer.objects.create(
        reference_id=reference_id,
        transaction_id=transaction_id,
        requested_at=requested_at,
        beneficiary=beneficiary_account,
        sender_partner_id=partner_id,
        remarks=remarks,
        amount=remittance_amount,
        currency=currency,
        status=status,
        channel=FundTransfer.INSTAPAY,
        fee=TRANSACTION_FEES.get('instapay', 30)
    )

    return transfer, result
