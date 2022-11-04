import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
from helpers.asset import create_manual_asset
from uuid import uuid4
from playwright.sync_api import expect
import variables

@pytest.mark.regression
def test_customer_new_manual_assets(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'IService' + str(uuid4()), first_name = 'John', last_name = 'Smith')
    customer.create(api_request_context)

    create_manual_asset(page, customer.customer_id, asset_type_name = 'Printer', name = 'Canon', asset_serial = str(uuid4()) )
    create_manual_asset(page, customer.customer_id, asset_type_name = 'Router', name = 'TPlink', asset_serial = str(uuid4()) )

    # Go to customer edit page, verify assets fields in the grid
    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')
    expect(page.locator('div.widget.overflowable:has-text("Assets") tr:has-text("Canon")')).to_contain_text("Printer")
    expect(page.locator('div.widget.overflowable:has-text("Assets") tr:has-text("TPlink")')).to_contain_text("Router")

    # Click on View all
    # Verify assets grid
    page.click('div.widget-header:has-text("Assets") a:has-text("View All")')
    expect(page.locator('div.col-md-5')).to_contain_text('All Assets')
    expect(page.locator('table.table-striped.borderless')).to_contain_text("Canon")
    expect(page.locator('table.table-striped.borderless')).to_contain_text("TPlink")
