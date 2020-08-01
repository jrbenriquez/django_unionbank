import hashlib
import random
import string

from django_unionbank.models import FundTransfer


def generate_callback_hash():
    string = "{}{}".format('UNIONBANK').encode('utf-8')
    return hashlib.md5(string).hexdigest()


def generate_ft_reference_id(method=None):
    METHOD_DICT = {
        'ubp': 'UBP',
        'instapay': 'IPY',
        'pesonet': 'PSO'
    }
    if method and method in METHOD_DICT:
        method_prefix = METHOD_DICT[method]
    else:
        method_prefix = None
    reference_id = ''.join([random.choice(string.digits) for i in range(8)])
    while FundTransfer.objects.filter(reference_id=reference_id).exists():
        reference_id = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in range(12)])
    return "{}{}".format(method_prefix, reference_id)
