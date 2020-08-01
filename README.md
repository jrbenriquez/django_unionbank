
#Django DragonPay

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
To be written soon.