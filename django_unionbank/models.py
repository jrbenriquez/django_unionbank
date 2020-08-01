# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class InstapayBank(models.Model):

    name = models.CharField(
        max_length=128)
    code = models.CharField(
        max_length=128)
    brstn = models.CharField(
        max_length=128, null=True, blank=True)
    remarks = models.CharField(
        max_length=128, null=True, blank=True)

    def __str__(self):
        return u"[{}] {}".format(self.code, self.name)


class PESONetBank(models.Model):

    name = models.CharField(
        max_length=128)
    code = models.CharField(
        max_length=128)
    brstn = models.CharField(
        max_length=128, null=True, blank=True)
    remarks = models.CharField(
        max_length=128, null=True, blank=True)

    def __str__(self):
        return u"[{}] {}".format(self.code, self.name)



class FundTransfer(models.Model):

    FUNDTRANSFER = 'UBP'
    INSTAPAY = 'IPY'
    PESONET = 'PSO'

    CHANNELS = (
        (FUNDTRANSFER, 'Fund Transfer'),
        (INSTAPAY, 'Instapay Fund Transfer'),
        (PESONET, 'PESONet Fund Transfer')
    )

    SUCCESS = "S"
    FAILED = "F"
    PENDING = "P"

    STATUS_CHOICES = (
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (PENDING, 'Pending')
    )

    reference_id = models.CharField(
        max_length=32, null=True, blank=True)
    transaction_id = models.CharField(
        max_length=32, null=True, blank=True)
    requested_at = models.DateTimeField()
    beneficiary = models.CharField(
        max_length=32, null=True, blank=True)
    sender_partner_id = models.CharField(
        max_length=64, null=True, blank=True)
    remarks = models.CharField(
        max_length=128, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    currency = models.CharField(
        max_length=8, default='PHP'
    )
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=PENDING)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    channel = models.CharField(choices=CHANNELS, max_length=8)
    sender_data = models.TextField(null=True, blank=True)
    beneficiary_data = models.TextField(null=True, blank=True)
    remittance_data = models.TextField(null=True, blank=True)

    def complete(self):
        self.status = self.SUCCESS
        self.completed_at = datetime.now()
        self.save()

    def failed(self, remarks='None'):
        self.status = self.FAILED
        self.remarks = remarks
        self.updated_at = datetime.now()
        self.save()


class SandBoxAccount(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    user_id = models.CharField(max_length=32)
    account_number = models.CharField(max_length=32)
    card_number = models.CharField(max_length=32)
    account_name = models.CharField(max_length=32)
    account_code = models.CharField(max_length=32)
    account_type = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    branch = models.CharField(max_length=32)
    balance = models.DecimalField(max_digits=12, decimal_places=2)



