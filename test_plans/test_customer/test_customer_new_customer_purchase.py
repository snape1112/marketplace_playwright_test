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

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')
    page.wait_for_timeout(100)
    time.sleep(1)
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child > a[class="btn btn-default btn-sm dropdown-toggle"]')
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child input[value="Customer Purchase"]')
    
    time.sleep(1)

    expect(page.locator('div.alert')).to_contain_text('Customer purchase was successfully created.')
    expect(page.locator('.widget-content > p > a:nth-child(2)')).to_contain_text(customer.business_name)

    page.click('span[data-bip-attribute=identification]:has-text("Click to add")')
    page.fill('span[data-bip-attribute=identification] input[type=text]', 'identify')
    page.click('span[data-bip-attribute=identification] input[type=submit]')

    page.click('span[data-bip-attribute=notes]:has-text("Click to add")')
    page.fill('span[data-bip-attribute=notes] textarea', 'notes')
    page.click('span[data-bip-attribute=notes] input[type=submit]')

    page.click('a:has-text("Attach File")')
    page.set_input_files('input#fsp-fileUpload', __file__)
    page.click('div.fsp-footer span[title="Upload"]')
    
    time.sleep(7)

    page.fill('.widget-content:has-text("Manual New Inventory") #customer_purchase_line_item_name', 'name')
    page.fill('#customer_purchase_line_item_description', 'description')
    page.select_option('#category_ids', label='Default')
    page.fill('#customer_purchase_line_item_serial_number', 'number')
    page.fill('#customer_purchase_line_item_condition', 'condition')
    time.sleep(1)
    page.click('.widget-content:has-text("Manual New Inventory") input:has-text("Add Item")')

    time.sleep(2)

    expect(page.locator('div.alert')).to_contain_text('Added the item')

    page.fill('#purchase_comment_body', 'comment')
    page.click('input:has-text("Add Comment")')

    time.sleep(2)

    expect(page.locator('div.alert')).to_contain_text('Added the comment')

