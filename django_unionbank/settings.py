from django.conf import settings

PROD_BASE_PATH = 'https://api.unionbankph.com/ubp/external'
UAT_BASE_PATH = 'https://api-uat.unionbankph.com/ubp/uat'
SANDBOX_BASE_PATH = 'https://api-uat.unionbankph.com/partners/sb'

USE_UNIONBANK_ONLINE = getattr(settings, 'USE_UNIONBANK_ONLINE', False)

if USE_UNIONBANK_ONLINE:


    UNIONBANK_CLIENT_ID = settings.UNIONBANK_CLIENT_ID

    UNIONBANK_CLIENT_SECRET = settings.UNIONBANK_CLIENT_SECRET

    UNIONBANK_PARTNER_ID = settings.UNIONBANK_PARTNER_ID

    UNIONBANK_USERNAME = settings.UNIONBANK_USERNAME
    UNIONBANK_PASSWORD = settings.UNIONBANK_PASSWORD

UNIONBANK_API_MODE = getattr(settings, 'UNIONBANK_API_MODE', None)

if UNIONBANK_API_MODE == 'PROD':
    UNIONBANK_API_BASE_PATH = PROD_BASE_PATH
elif UNIONBANK_API_MODE == 'UAT':
    UNIONBANK_API_BASE_PATH = UAT_BASE_PATH
elif UNIONBANK_API_MODE == 'SANDBOX':
    UNIONBANK_API_BASE_PATH = SANDBOX_BASE_PATH
else:
    if USE_UNIONBANK_ONLINE:
        raise Exception('UNIONBANK_API_MODE not set. Choices are: "PROD", "UAT" & "SANDBOX", please set.')


