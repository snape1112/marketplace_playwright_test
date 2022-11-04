import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
def test_customer_validate_printing_options(page, login, api_request_context):

    # Enable show Print button
    api_url = f'{variables.base_url}/api/v1/settings/printing'
    api_headers = { "Accept": "application/json","Content-Type": "application/json","Authorization": variables.token}
    api_request_context.get(api_url, headers=api_headers)

    # Preconditions: create customer
    customer = Customer(business_name = 'IService' + str(uuid.uuid4()), first_name = 'John', last_name = 'Smith')
    customer.create(api_request_context)
    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')

    page.click('a.dropdown-toggle span[data-original-title="print"]')

    # Verify that Customer Label item has href to Customer Label print
    href = page.locator('div.open a.menu-default:has-text("Customer Label")').get_attribute('href')
    assert href == f'/customers/{customer.customer_id}/print'

    # Verify that Address Label item has href to Address Label print
    href= page.locator('div.open a.menu-default:has-text("Address Label")').get_attribute('href')
    assert href[0:14] == '/labels?labels'
