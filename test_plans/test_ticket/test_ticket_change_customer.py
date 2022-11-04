import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import Ticket
from playwright.sync_api import expect
from time import sleep
import variables

@pytest.mark.regression
def test_ticket_change_customer(page, login, api_request_context):
    first_customer_name = "First customer" + str(uuid.uuid4())
    customer_id, _ = create_customer(first_customer_name, api_request_context)

    second_customer_name = "Second customer" + str(uuid.uuid4())
    second_customer_id, _ = create_customer(second_customer_name, api_request_context)

    ticket = Ticket(customer_id = customer_id)
    ticket.create(api_request_context)
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')
    page.click('div.widget-header a:has-text("Change")')
    page.type('input#ticket_customer_name', second_customer_name[:8])
    page.click(f'text=/{second_customer_name[:10]}.*/')
    page.click('input:has-text("Change")')
    sleep(5)
    expect(page.locator(f'span.tooltipper a[href="/customers/{second_customer_id}"]')).to_contain_text(second_customer_name[:10])