import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import variables

@pytest.mark.regression
def test_ticket_split(page, login, api_request_context):
    # Prerequisites
    customer_name = str(uuid.uuid4()) 
    customer_id, _  = create_customer(customer_name, api_request_context) 
    ticket_id, ticket_num = create_ticket(customer_id, api_request_context)
    page.once("dialog", lambda dialog: dialog.accept())
    
    # Split
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}')
    assert page.locator(f'text={ticket_num}') != None
    page.click('text=Actions')
    page.click('text=Split')
    page.fill(f'#split_new_subject', 'Split from ' +str(ticket_num))
    page.select_option('#split_new_status', value='In Progress')
    page.click('input:has-text("Split Ticket")')

    # Verify
    expect(page.locator('text="split complete!!"')).to_be_visible()
    expect(page.locator(f'text="Split from {ticket_num}"')).to_be_visible()
    expect(page.locator(f'text="End of history from {ticket_num}"')).to_be_visible()
    expect(page.locator(f'text="Ticket split off from {ticket_num}"')).to_be_visible()