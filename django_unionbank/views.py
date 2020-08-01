# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_unionbank import settings
from django_unionbank.api.customer import customer_code_for_token

# Create your views here.


def customer_auth_callback(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        grant_type = "authorization_code"

        data = {
            "code": code,
            "grant_type": grant_type
        }

        token_data = customer_code_for_token(data)
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')

        """
        {
            'token_type': 'bearer',
            'access_token': 'AAIkMzRkMDEyYWQtMDQ5Ni00ODFhLWFjZTEtYmRiNDhhMWUyYjYznlOdAOBCh5Ut7JmYMIOlSpXbJXLW_Jth9SbOYSJl7k3VHfUrl2I_vV0vqtCqsFWWExosADFboA6qLpRvMXbvmgj_fDoSWrUPDmIxGUVSYHt2yn9qBfNJrBgAr_K3867p9-CJU8NQVvGF4HXapFIF_LiNv3PAr75z9PE3iz6X-BUss11sl297_gf7fTSyilqkUV1RccIXr9OdcZqA4ZRLr4cPvZ4hCqT_tEjzmAfAqNo62OSJDwfZ50hFrDquB15SRT9ByiWQHDQDkNS6H1fi57JhqRSp6ZATsbjz1axKhzJU6I1Dm_-xTOkriBcJMWuCugR5mKIdUbgr15xM499QsWFudtjZjTHna3xq38PXtAqMYtrwj9QKGWP6W4Sq6PKDFsJJ2C12zzPtrUWg_M6d9ypQ2Qb96dyiRowYRXS4IXJTLy2sZ-C4RRJ0Uu7s_bWa',
            'metadata': 'a:rY5CFD9ja3as2I/pjQpncUHkPT7nt4GfJrI1FJd4uCvTDvaL4zLWgPXHYMyjAB/ccSO9PM9BoR20awD10P5LFigcgXO7fQHp1EGPzrrE47ZK6OBDsqD0JHWofSVV0BlbWdl3LCPBf47k3RMtiwy0iHoyUjsN7oX9/P 4',
            'expires_in': 31536000, 'consented_on': 1596188458,
            'scope': 'transfers instapay pesonet transfers_pesonet account_inquiry account_info',
            'refresh_token': 'AAIh9tGSkWPjNtnYSEwYZgv3mFZj6GqPcbK3VARoYHW1PeVwmesfEenD566XylQ49tAASWa-EIMVM3a8XpBrMxeyjh3rCkJj0U5gwEu-ZD0EkM4-s-_-rWlCGAk88Dlwmup0JUUI42nRcR4d-Qng7ybK-EqTm6n6bNdnLoO4UYSMtoZd0avbt9hUEMFlQh-SbJmA-ktL4HdWhcbryazIXh0V7yexHcRchvPjzQjPevdBLYrIR6ZfkV2IH_Eq2dHyELjLP7aKo7J4iogVmS3OljkUrafF7_taWFNMfiJwpiXovz4Ym0UkdjQzzGq8of1QnimsdpwThhwtGGBx64XIMH3Zap1Ox2c8priJ_pCdc6y177lcvsyOQ3wzuW3Z5n9H60sDWnnWOqnEIhh-V4qT0HSJMLJnlEhkF6VY_T8zfpKclBopXdvTXN_ll22EpXNeLYm-kC1R9wPYFxKcDqxX1dtB',
            'refresh_token_expires_in': 2682000
        }
        """
