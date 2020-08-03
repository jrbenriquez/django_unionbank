
# django_unionbank

Django Unionbank is the library for easily integrating and consuming the Unionbank of the Philippines API with your Django Application. As of now this has been used in production for Partner Accounts(Corporate) Fund Transfers (UBP, Instapay, PESOnet) to any bank accounts and will eventually add Customer Account services as well. Codebase is functioning but still currently for standard refactoring/development and testing :)

Quick Start
-----------

0. To install, use pip:

        pip install django_unionbank

1. Add django_unionbank to you INSTALLED_APPS settings like this:
        
        INSTALLED_APPS = [
        ...,

        'django_unionbank',

        ...
        ]

2. Configure django_unionbank by adding these to your settings.py::

        USE_UNIONBANK_ONLINE=True
        UNIONBANK_CLIENT_ID=<REPLACE WITH CLIENT ID>
        UNIONBANK_CLIENT_SECRET=<REPLACE WITH CLIENT SECRET>
        UNIONBANK_PARTNER_ID=<REPLACE WITH PARTNER ID>
        UNIONBANK_API_MODE=<CHOOSE FROM SANDBOX, UAT, PROD>
        UNIONBANK_USERNAME=<REPLACE USERNAME>
        UNIONBANK_PASSWORD=<REPLACE PASSWORD>


3. Library allows you to have certain models used to save FundTransfer Data,  SandBox Accounts, Data of Instapay and PESONet banks available. For now, saving data in the database is required to function. To do this:

        python manage.py migrate django_unionbank

Usage
-----

## Partner Authentication

1. **UnionBank Partner Authentication**

    **get_partner_token**
    
        from django_unionbank.api.partner_authentication import get_partner_token
        
        token = get_partner_token(scope)
        
    Parameters:
    
    * __scope__: [str] Space separated OAuth2 scopes. See https://developer.unionbankph.com/reference#tag/OAuth2-Scopes for complete list of scopes

    Returns:
    token = [str] Online partner access token

## Partner Transfers

1. **Unionbank Partner Account to Unionbank Account Fund Transfer**

    **partner_funds_transfer**
    
        from django_unionbank.api.identity.partner_funds_transfer
        
        transfer, message = partner_funds_transfer(token, account_number, amount, remarks="Partner Payout")

    Parameters:
    
    * __token__: [str] Partner access token you can retrieve using **get_partner_token** method
    * __account_number__: [str] Valid Unionbank Account Number
    * __remarks__: [str] Remarks for the specific transaction
    * __amount__:[str/decimal] Amount to transfer
    * __currency__: [str] __default='PHP'__ Object containing additional info you want to include in transaction
    * __reference_id__: [str] If not provided, package has default id generator (UBPXXXX, IPYXXXX, PSOXXXX)
    * __info__: [list] Object containing additional info you want to include in transaction
    
    Returns:
    * transfer = FundTransfer object. Check models.py
    * message = Response message
        
            sample_info = [
                {
                    "index": "1",
                    "name": "Recipient",
                    "value": "Juan dela Cruz"
                },
                {
                    "index": "2",
                    "name": "Message",
                    "value": "Sample Message"
                },
                {
                    "index": "3",
                    "name": "Custom Info",
                    "value": "Custom Value"
                }
            ]        

2. **Unionbank Partner Account InstaPay Transfer**

    **partner_instapay_fund_transfer**
    
        from django_unionbank.api.instapay.partner_instapay_fund_transfer
        
        transfer, message = partner_instapay_fund_transfer(token, data)

    Parameters:
    
    * __token__: [str] Partner access token you can retrieve using **get_partner_token** method
    * __data__: [list] Information regarding transfer to be made in the following prescribed format
    * __reference_id__: [str] If not provided, package has default id generator (UBPXXXX, IPYXXXX, PSOXXXX)
    
    Returns:
    * transfer = FundTransfer object. **Check models.py
    * message = Response message
        
            data = {
                'sender_name': <[str] SENDER NAME>,
                'sender_address': {
                        "line1": <[str]>,
                        "line2": <[str]>,
                        "city": <[str]>,
                        "province": <[str]>,
                        "zipCode": <[str]>,
                        "country": <[str]>
                    },
                'beneficiary_account': <[str] RECIPIENT ACCOUNT NUMBER>,
                'beneficiary_name': <[str] RECIPIENT ACCOUNT NAME>,
                'beneficiary_address': {
                        "line1": <[str]>,
                        "line2": <[str]>,
                        "city": <[str]>,
                        "province": <[str]>,
                        "zipCode": <[str]>,
                        "country": <[str]>
                    },
                'remittance_amount': <[str/decimal] TRANSFER AMOUNT>,
                'remittance_bank': <[int] InstaPay bank code - see "update_instapay_banks" method for data of valid bank with codes>
                'remittance_purpose': <1001 or 1002 or 1003>,
                'remittance_instructions': <[str] Optional Instructions/Remarks here>
            }


3. **Unionbank Partner Account PESONet Transfer**

    **partner_pesonet_fund_transfer**
    
        from django_unionbank.api.pesonet.partner_pesonet_fund_transfer
        
        transfer, message = partner_pesonet_fund_transfer(token, data)

    Parameters:
    
    * __token__: [str] Partner access token you can retrieve using **get_partner_token** method
    * __data__: [list] Information regarding transfer to be made in the following prescribed format
    * __reference_id__: [str] If not provided, package has default id generator (UBPXXXX, IPYXXXX, PSOXXXX)
    
    Returns:
    * transfer = FundTransfer object. **Check models.py
    * message = Response message
        
            data = {
                'senderRefId': <[str] Reference ID here]>,
                "tranRequestDate": <[str] Datetime ISO Format (i.e. datetime.now().isoformat()[:-3]>,
                "sender": {
                    "name": <[str] Sender Name]>,
                    "address": {
                                "line1": <[str]>,
                                "line2": <[str]>,
                                "city": '<[str]>',
                                "province": <[str]>,
                                "zipCode": <[str]>,
                                "country": <[str]>
                    }
                },
                "beneficiary": {
                    "accountNumber": <str> RECIPIENT ACCOUNT NUMBER>,
                    "name": <str> RECIPIENT NAME>,
                    "address": {
                                "line1": <[str]>,
                                "line2": <[str]>,
                                "city": <[str]>,
                                "province": <[str]>,
                                "zipCode": <[str]>,
                                "country": <[str]>
                    }
                },
                "remittance": {
                    "amount": <[str] representation of amount with 2 decimal places>>,
                    "currency": <[str] 'PHP'>,
                    "receivingBank": <[int] InstaPay bank code - see "update_pesonet_banks" method for data of valid banks with codes>,
                    "purpose": <1001, 1002, 1003>,
                    "instructions": <[str] Optional Instructions/Remarks here>
                }
            }
    

## InstaPay and PESONet partner banks

- **update_instapay_banks** and **update_pesonet_banks**
    
    Returns: list of partner banks for the respective service
        
Calling these methods allows you to save all partner banks available to the database mapped via the InstapayBank and PESONetBank models respectively

    from django_unionbank.api.instapay import update_instapay_banks
    from django_unionbank.api.instapay import update_pesonet_banks
    
    instapay_bank_list = update_instapay_banks()
    pesonet_bank_list = update_pesonet_banks()
    
    # model classes available in: django_unionbank.models.py
    

## Partner Account Balance

- **get_last_running_balance**

    Returns:
        balance = Remaining Balance on the account
        records = last 10 activity/transaction records
        record_count = total record/activity count in account
        
    
        from django_unionbank.api.identity import get_last_running_balance
    
        balance, records, record_count = get_last_running_balance()
       
    
          
        
          
        

