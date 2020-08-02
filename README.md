
# django_unionbank

Django Unionbank is the library for easily integrating and consuming the Unionbank of the Philippines API with your Django Application. As of now this has been used in production for Partner Accounts(Corporate) Fund Transfers (UBP, Instapay, PESOnet) and will eventually add Customer Account services as well. Codebase is functioning but still for standard refactoring, testing and packaging for PIP :)

Quick Start
-----------

0. To install, use pip::

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


3. Library allows you to have certain models used for SandBox Accounts, Keeping a copy of the Instapay and PESONet banks available. For now, saving data in the database is required to function. To do this:

        python manage.py migrate django_unionbank

Usage
-----
#### Partner Transfers

1. **Unionbank Partner Account to Unionbank Account Fund Transfer**

    **partner_funds_transfer**
    
        from django_unionbank.api.identity.partner_funds_transfer
        
        partner_funds_transfer(token, account_number, amount, remarks="Partner Payout")

    Parameters:
    
    * __token__: [str] Partner access token you can retrieve using **get_partner_token** method
    * __account_number__: [str] Valid Unionbank Account Number
    * __remarks__: [str] Remarks for the specific transaction
    * __amount__:[str/decimal] Amount to transfer
    * __currency__: [str] __default='PHP'__ Object containing additional info you want to include in transaction
    * __info__: [list] Object containing additional info you want to include in transaction
    
        
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
        

