import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
import variables

@pytest.mark.regression
def test_ticket_cancel(page, login, api_request_context):
    # Prerequisites
    customer_name = str(uuid.uuid4()) 
    customer_id, _ = create_customer(customer_name, api_request_context) 
    ticket_id, ticket_num = create_ticket(customer_id,api_request_context)

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}')
    
    page.once("dialog", lambda dialog: dialog.accept())
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}')
    assert page.locator(f'text={ticket_num}') != None
    page.click('text=Actions')
    page.click('text=Cancel')
    assert page.wait_for_selector('text="Ticket was cancelled!"') != None