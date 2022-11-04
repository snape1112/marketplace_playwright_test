import uuid
from uuid import uuid4

import pytest
import variables
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer, create_customer
from helpers.invoice import create_new_invoice
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import time

@pytest.mark.regression
def test_invoice_add_payment(page, login, api_request_context):
    customer = Customer(business_name = 'IService' + str(uuid4()), first_name = 'John', last_name = 'Smith')
    customer.create(api_request_context)

    # Pre-condition

    customer_name = customer.business_name
    create_customer(customer_name, api_request_context)
    create_new_invoice(page, customer_name)
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/invoices')

    # Create the line item

    page.click(f"text=/{customer_name[:5]}.*/")
    page.type('#line_item_item','Labor', delay=150)
    page.click('text="Labor - Labor"')   
    page.click('text=Create Line item')
    page.click('[data-bip-attribute=price]')
    page.fill('input[name="price"]', "300")
    with page.expect_navigation():
        page.click('input:has-text("Save")')

    time.sleep(1)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')
    page.wait_for_timeout(100)
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child > a[class="btn btn-default btn-sm dropdown-toggle"]')
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child a:has-text("Payment")')
    
    time.sleep(1)
    page.fill('input[class="string applyAmountBox"]', "300")
    page.click("input[value='Take Payment']")

    time.sleep(1)

    assert page.locator('div.alert:has-text("Payment successfully applied")').inner_text() != None
    

