

# Unionbank Possible Scopes

AUTH_SCOPES = {
    'payments': 'Allow bills payment via partner',
    'transfers': 'Allow funds transfer via partner',
    'transfers_pesonet': 'Allow Pesonet transfer via partner',
    'instapay': 'Scope path for Instapay transfer',
    'prepaid_transfers': 'Scope path for prepaid transfer',
    'buy_load': 'Scope path for buy load',
    'paymaya': 'Scope path for Paymaya transfers',
    'coins': 'Scope path for Coins.ph transfers',
    'load_purchase': 'Scope path for Load purchases',
    'swift': 'Scope path for SWIFT transactions',
    'card_perks': 'Scope path for Card perks',
    'rtgs': 'Scope path for RTGS Transactions',
    'otp': 'Scope path for OTP Transactions',
    'payments_loans': 'Scope path for Loan Payments',
    'account_inquiry': 'Scope path for Partner Account Transaction History',
    'eon_transfers': 'Scope path for Partner Eon Top Up',
    'interblocks': 'Scope path for Partner Prepaid Top Up via IBL',
    'link_account': 'Scope path for Unlink Account API',
    'oda_loans': 'Scope path for Overdraft Account API',
    'account': 'Scope path for Loan Payment API, Scope path for Loan Availment API',
}


INSTAPAY_BANKS = {
    148120: "Sun Savings Bank",
    161311: "Asia United Bank",
    161312: "Banco De Oro Unibank, Inc.",
    161336: "JPMorgan Chase Bank",
    161341: "Metropolitan Bank and Trust Co",
    161398: "Chinabank",
    161399: "Chinabank Savings",
    161400: "Chinatrust Banking Corp",
    161401: "Eastwest Bank",
    161402: "Equicom Savings Bank",
    161403: "Omnipay",
    161404: "Paymaya",
    161405: "PSBank",
    161406: "Robinsons Bank",
    161407: "UCPB",
    161408: "UnionBank",
    161409: "RCBC Bank",
    161410: "Landbank Of The Phils",
    161411: "Yuanta Savings Bank",
    161412: "Philtrust Bank",
    161414: "G-Exchange, Inc."
}

PESONET_BANKS = {
    161203: "Bank Of China",
    161207: "Sterling Bank Of Asia",
    161215: "Mega Intl Comml Bank Co. Ltd",
    161223: "China Bank Savings",
    161226: "Equicom  Savings Bank, Inc.",
    161227: "First Consolidated Bank Inc.",
    161245: "Tong Yang Savings Bank,Inc.",
    161309: "Australia and New Zealand Bank",
    161311: "Asia United Bank",
    161312: "Banco De Oro Unibank, Inc.",
    161315: "Bangkok Bank Public Co., Ltd.",
    161316: "Bank Of America, Nat'l. Ass'n.",
    161317: "Bank Of Commerce",
    161319: "Bank Of The Philippine Islands",
    161322: "China Banking Corporation",
    161324: "Citibank N.A.",
    161326: "Devt. Bank Of The Phils.",
    161327: "Deutsche Bank",
    161329: "East-West Banking Corporation",
    161334: "HK and Shanghai Banking Corp.",
    161336: "JPMorgan Chase Bank",
    161338: "Land Bank Of The Philippines",
    161340: "Maybank Phils.,Inc.",
    161341: "Metropolitan Bank and Trust Co",
    161342: "Mizuho Bank, Ltd.",
    161345: "Phil. Bank Of Communications",
    161346: "Philippine National Bank",
    161347: "Philippine Savings Bank",
    161348: "Philippine Trust Company",
    161349: "Philippine Veterans Bank",
    161353: "Rizal Commercial Banking Corp.",
    161354: "Robinsons Bank Corporation",
    161360: "Security Bank Corporation",
    161362: "The Standard Chartered Bank",
    161365: "United Overseas Bank Phils.",
    161415: "United Coconut Planters Bank",
    161416: "Union Bank of the Philippines",
    161417: "MUFG Bank, Ltd",
    161418: "CTBC Bank (Philippines) Corp.",
    161419: "Keb Hana Bank",
    161420: "First Consolidated Bank",
    161421: "Sumimoto Mitsui Banking Corp",
    161422: "Shinhan Bank",
    161423: "Industrial Bank of Korea - Manila",
    161424: "Wealth Development Bank",
    161425: "Al-Amanah Islamic Investment Bank",
    161426: "Producers Savings Bank Corporation"
}

TRANSACTION_FEES = {
    "instapay": '30',
    "pesonet": '25'
}

INSTAPAY_RESPONSE_CODES = {
    "TS": 'Transaction Success',
    "TF": 'Transaction Failed',
    "SC": 'Sent for Confirmation',
    "SP": 'Sent for Processing'
}