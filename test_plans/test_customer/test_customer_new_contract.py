import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
from uuid import uuid4
from playwright.sync_api import expect
import variables

@pytest.mark.regression
def test_customer_new_contracts(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'IService' + str(uuid4()), first_name = 'John', last_name = 'Smith')
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')
    page.click('div.widget-header:has-text("Contracts") a:has-text("New")')
    page.type('input#contract_name', 'Test contract name')

    page.type('input#contract_contract_amount', '60000')
    page.select_option('select#contract_likelihood', value='75')
    page.type('textarea#contract_description', 'Test Description')
    page.wait_for_timeout(2000)
    page.click('text="Create Contract"')
    assert page.wait_for_selector("text=Contract was successfully created")

    # Go to contracts page
    page.goto(f'{variables.base_url}/contracts')

    # Verify Contract grid fields on the contracts page
    expect(page.locator('table.table-striped.borderless')).to_contain_text('Test contract name')
    expect(page.locator('table.table-striped.borderless:has-text("Test contract name")')).to_contain_text(customer.business_name)
    expect(page.locator('span[data-bip-attribute="contract_amount"]')).to_contain_text('$60,000')
    expect(page.locator('span[data-bip-attribute="status"]')).to_contain_text('Opportunity')
    expect(page.locator('span[data-bip-attribute="likelihood"]')).to_have_text('75')

    # Go to customer page
    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')

    # Verify Contract grid fields on the customer page
    expect(page.locator('div.widget:has-text("contracts") tr:has-text("Test contract name")')).to_contain_text('$60,000.00')
    expect(page.locator('div.widget:has-text("contracts") tr:has-text("Test contract name")')).to_contain_text('Opportunity')

