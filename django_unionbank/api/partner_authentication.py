import requests
import json

from django_unionbank.constants import AUTH_SCOPES
from django_unionbank import settings as ub_settings
# from django_unionbank.models import AccessToken


def get_partner_token(scope):
    PRODUCT_NAME = 'Partner Authentication'
    ENDPOINT_URL = '{}{}'.format(
        ub_settings.UNIONBANK_API_BASE_PATH,
        '/partners/v1/oauth2/token'
    )

    # Check Scope
    if scope not in AUTH_SCOPES:
        raise Exception('Invalid Scope')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html'
    }

    payload = {
        'grant_type': 'password',
        'client_id': ub_settings.UNIONBANK_CLIENT_ID,
        'username': ub_settings.UNIONBANK_USERNAME,
        'password': ub_settings.UNIONBANK_PASSWORD,
        'scope': scope
    }

    response = requests.post(url=ENDPOINT_URL, data=payload, headers=headers)

    response_data = json.loads(response.text)

    if response_data.get('httpCode', None) == '401' and \
        response_data.get('httpMessage', None) == 'Unauthorized' and \
        response_data.get('moreInformation', None) == 'Not registered to plan':

        raise Exception('Not Registered to required plan for {}'.format(PRODUCT_NAME))

    if response.status_code != requests.codes.ok:
        raise Exception('Something went wrong: {}'.format(response.text))

    # TODO Best practices shouled we store access tokens? or not.
    # access = AccessToken.objects.create(
    #     token_type=response_data['bearer'],
    #     token=response_data['access_token'],
    #     metadata=response_data['metadata'],
    #     expires_in=response_data['expires_in'],
    #     scope=response_data['scope'],
    #     refresh_token=response_data['refresh_token'],
    # )

    return response_data['access_token']



