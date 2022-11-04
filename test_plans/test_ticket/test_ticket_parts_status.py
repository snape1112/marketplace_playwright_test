import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket, create_parts_status_entry 
import variables

@pytest.mark.regression
def test_ticket_parts_status(page, login, api_request_context):
    # Prerequisites
    customer_name = str(uuid.uuid4()) 
    customer_id, _  = create_customer(customer_name, api_request_context) 
    # The _ is the perferred way of trashing variables you don't use.
    ticket_id, _ = create_ticket(customer_id, api_request_context)
    _, item_id = create_parts_status_entry(page, ticket_id)

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}')
    page.click('text=Add/View Charges')
    assert page.locator(f'text=PartOrder-{item_id}') != None
    # Note:  It would be good to capture the line item ID and make it available.