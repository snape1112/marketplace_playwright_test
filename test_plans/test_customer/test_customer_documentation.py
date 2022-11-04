import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
from uuid import uuid4
from playwright.sync_api import expect
import variables

@pytest.mark.regression
def test_customer_documentation(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'IService' + str(uuid4()))
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')

    # Create new documentation
    page.click('div.widget-header:has-text("Documentation") a:has-text("New")')
    page.wait_for_timeout(8000)
    page.click('div.mce-edit-area > iframe')
    page.keyboard.type('1 Test Documentation text')

    page.click('text=Save Page')

    assert page.wait_for_selector('text=Wiki page was successfully created')

    expect(page.locator('div.usercontent')).to_contain_text('Test Documentation text')

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')

    # Verify that documentation exist on the customer show page
    expect(page.locator('div.widget.borderless:has-text("documentation")')).to_contain_text(customer.business_name)
    expect(page.locator('div.widget.borderless:has-text("documentation")')).to_contain_text('Internal')
