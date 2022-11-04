import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import variables
from helpers.quick_view import validate_customer_quick_view

@pytest.mark.regression
def test_ticket_validate_new_options(page, login, api_request_context):
    customer_name = str(uuid.uuid4())
    customer_id, _ = create_customer(customer_name, api_request_context)
    create_ticket(customer_id, api_request_context)

    validate_customer_quick_view(page, customer_id, f'{variables.base_url}/tickets')
