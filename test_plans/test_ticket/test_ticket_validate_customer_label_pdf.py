from time import sleep
import time
import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import variables

def test_ticket_validate_customer_label_pdf(page, login, api_request_context):
    customer_name = str(uuid.uuid4())
    customer_id, _  = create_customer(customer_name, api_request_context)
    quick_view_selector = '#quick-view-customer-{}'.format(customer_id)
    create_ticket(customer_id, api_request_context)
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)
    page.click('a[class="btn btn-default dropdown-toggle  tooltipper"] > i[class="fas fa-caret-down"]')
    # Verify that Customer Label item has href to Customer Label pdf
    href = page.locator('text=Customer Label').get_attribute('href')
    assert href == f'/customers/{customer_id}.pdf'
