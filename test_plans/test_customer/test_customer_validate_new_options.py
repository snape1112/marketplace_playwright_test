import pytest
from fixtures import constants
from fixtures.login import create_account, login
from helpers.customer import Customer
from playwright.sync_api import expect
from uuid import uuid4
import variables
from helpers.quick_view import validate_customer_quick_view

@pytest.mark.regression
def test_customer_validate_new_options(page, login, api_request_context):

    # Preconditions: create customer

    customer = Customer(business_name = 'John' + str(uuid4())[1:10])
    customer.create(api_request_context)

    validate_customer_quick_view(page, customer.customer_id, f'{variables.base_url}/customers')
