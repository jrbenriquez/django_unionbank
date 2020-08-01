
from django.conf.urls import url, include, static

from django_unionbank import views
from django_unionbank.utils import generate_callback_hash


urlpatterns = [
    url(r'', views.customer_auth_callback, name='customer_auth_callback'),
]
