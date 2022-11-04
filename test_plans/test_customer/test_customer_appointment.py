import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
from helpers.appointment import validate_appointment
from helpers.asset import create_manual_asset
from uuid import uuid4
import variables

@pytest.mark.regression
def test_customer_appointment(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'IService' + str(uuid4()))
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')

    validate_appointment(page, customer.business_name, 'Phone Call', 'Morning of and 1 hour before')
