import pytest
from fixtures import constants
from helpers.customer import Customer
from fixtures.login import create_account, login
from playwright.sync_api import expect
from uuid import uuid4
import variables

@pytest.mark.regression
def test_customer_archive(page, login, api_request_context):

    # Preconditions: create customer

    customer = Customer(business_name = 'John' + str(uuid4())[1:10])
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')
    page.click('div.row.mbm a.btn.btn-default:has-text("Actions")')
    # Let the Flash messages to clear.
    # We need to wait Flash from the next page on the current page
    page.on("dialog", lambda dialog: dialog.accept())
    page.wait_for_timeout(3000)

    # Click 'Archive'
    page.click('li:has-text("Archive")')

    expect(page.locator('div.main')).not_to_contain_text(customer.business_name)
    expect(page.locator('div.error-container-thingy')).to_contain_text('Customer was archived.')

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')

    expect(page.locator('div.alert.alert-danger')).to_contain_text('Customer is Archived')

    page.click('div.row.mbm a.btn.btn-default:has-text("Actions")')
    page.on("dialog", lambda dialog: dialog.accept())
    # Let the Flash messages to clear
    page.wait_for_timeout(3000)

    # Click 'Re-Enable'
    page.click('li:has-text("Re-Enable")')

    expect(page.locator('div.error-container-thingy')).to_contain_text('Customer was enabled.')


    page.goto(f'{variables.base_url}/customers/')
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer.business_name)
