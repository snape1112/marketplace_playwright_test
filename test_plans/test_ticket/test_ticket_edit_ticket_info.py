import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import Ticket
from playwright.sync_api import expect
from time import sleep
from helpers.ticket import wait_for_worker
import variables

def edit_subscribers(page):
    wait_for_worker(page, 'tr:has-text("Subscribers")')
    # Subscribe tech
    page.click('a.dropdown-toggle:has-text("Actions")')
    page.click('ul.dropdown-menu button:has-text("Subscribe")')
    # Verify that tech was added to the ticket as subscriber
    expect(page.locator('tr:has-text("Subscribers")')).to_contain_text(variables.admin_name)

def edit_additional_carbon_copy(page):
    # Click on pencil icon on the ticket info field
    page.click('span.tooltipper a.bhv-CCsEdit i.fa-pencil')
    page.click('div#ticket_notify_emails_tagsinput')

    # Type 2 emails separated by comma to the Additional CC(carbon copy)
    page.type('div#ticket_notify_emails_tagsinput', 'test1@syncromsp.com,test2@syncromsp.com,')
    page.click('div.bhv-CCsEdit input[value="Submit"]')
    page.locator('span.bhv-CCsEdit div[style="mergin-left"]')

    # Verify that emails were added to the ticket info
    expect(page.locator('span.bhv-CCsEdit')).to_contain_text("test1@syncromsp.com")
    expect(page.locator('span.bhv-CCsEdit')).to_contain_text("test2@syncromsp.com")

@pytest.mark.regression
def test_ticket_edit_ticket_info(page, login, api_request_context):

    # Create customer
    customer_name = 'Customer'+ str(uuid.uuid4())
    customer_id, _  = create_customer(customer_name, api_request_context)

    # Create ticket
    ticket = Ticket(customer_id = customer_id)
    ticket.create(api_request_context)

    # Go to ticket page
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')

    edit_subscribers(page)
    edit_additional_carbon_copy(page)
