import pytest
from fixtures.constants import *
import uuid
import re
import json
import requests
import types
from fixtures.login import create_account, login
from helpers.api_token import generate_api_token
from playwright.sync_api import Page
import variables

# Use keyword arguments to make this method reusable and create multiple diffrent customers
# Base usage is still the same: create_customer("name", api_request_context)
# Customized usage: create_customer("name", api_request_context, first_name = "John", phone = "123456789")
def create_customer(name: str, api_request_context, **kwargs):

    """
        Creates a new customer
        Arguments:
            customer_name: a string
        Returns:
            Creates the new customer with the given name and returns the database id
    """
    # Data to send
    first_name = kwargs.get('first_name') or str(uuid.uuid4())
    last_name = kwargs.get('last_name') or str(uuid.uuid4())
    email = kwargs.get('email') or (str(uuid.uuid4())+'@syncromsp.com')

    notification_email = (str(uuid.uuid4())+'@syncromsp.com')

    # API POST call to customers
    response = api_request_context.post(
        f'https://{variables.subdomain}.{BASE_DOMAIN}/api/v1/customers',
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": variables.token,
        },
    data={
    "firstname": first_name,
    "business_name": name,
    "lastname": last_name,
    "email": email,
    "phone": kwargs.get('phone') or "14256545665",
    "address": kwargs.get('address') or "string",
    "address_2": kwargs.get('address_2') or "string",
    "city": kwargs.get('city') or "string",
    "state": kwargs.get('state') or "string",
    "zip": "string",
    "notes": "string",
    "get_sms": 0,
    "opt_out": 0,
    "no_email": 0,
    "get_billing": 0,
    "get_marketing": 0,
    "get_reports": 1,
    "ref_customer_id": 1,
    "referred_by": "string",
    "tax_rate_id": 0,
    "notification_email": f'{notification_email}',
    "invoice_cc_emails": "string",
    "invoice_term_id": 0,
    "properties": {},
    "consent": {}
     }

    )
    # Asserting that response is 200 and returning id
    assert response.ok
    customer_id = response.json()['customer']['id']
    return customer_id, email

# Customer class is used to pack customer attributes together and simplify
# tests that operate multiple customers
class Customer:
    def __init__(self, **kwargs):
        self.business_name = kwargs.get('business_name') or str(uuid.uuid4())
        self.first_name = kwargs.get('first_name') or str(uuid.uuid4())
        self.last_name = kwargs.get('last_name') or str(uuid.uuid4())
        self.phone = kwargs.get('phone')  or "14256545665"
        self.customer_id = None # I think id is reserved by Python
        self.email = kwargs.get('email') or (str(uuid.uuid4())+'@syncromsp.com')
        self.address = kwargs.get('address') or "string"
        self.address_2 = kwargs.get('address_2') or "string"
        self.city = kwargs.get('city') or "string"
        self.state = kwargs.get('state') or "string"

    def create(self, api_request_context):
        self.customer_id, _ = create_customer(self.business_name, api_request_context,
        first_name = self.first_name,
        last_name = self.last_name,
        phone = self.phone,
        email = self.email,
        address = self.address,
        address_2 = self.address_2,
        city = self.city,
        state = self.state
        )
