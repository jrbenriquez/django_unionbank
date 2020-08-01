RECEIVED_REQUEST = 'RT'
REQUEST_SUCCESS = 'TS'
REQUEST_FAILED = 'TF'
REQUEST_PROCESSING = 'SP'
NETWORK_ISSUE = 'NC'
CONFIRMING_REQUEST = 'SC'


UNIONBANK_RESPONSE_CODES = {
    RECEIVED_REQUEST: {
        'message': 'Received Transaction Request',
        'apis': 'all',
        'description': 'Transaction has reached UnionBank'},
    REQUEST_SUCCESS: {
        'message': 'Credited Beneficiary Account',
        'apis': 'all',
        'description': 'Successful transaction'},
    REQUEST_FAILED: {
        'message': 'Failed to Credit Beneficiary Account',
        'apis': 'all',
        'description': 'All transactional APIs	Transaction has failed'},
    REQUEST_PROCESSING: {
        'message': 'Sent for Processing',
        'apis': 'all',
        'description': 'Transaction is sent for processing'},
    NETWORK_ISSUE: {
        'message': 'Network Issue - Core',
        'apis': 'all',
        'description': 'Transaction has encountered a network issue'},
    CONFIRMING_REQUEST: {
        'message': 'Sent for Confirmation',
        'apis': 'instapay',
        'description': 'Transaction status for confirmation'},
}

PENDING_RESPONSE = [
    RECEIVED_REQUEST,
    REQUEST_PROCESSING,
    CONFIRMING_REQUEST
]