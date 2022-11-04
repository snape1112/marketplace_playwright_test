import pytest
from fixtures import constants
from fixtures.login import create_account, login
from helpers.customer import Customer
from helpers.invoice import create_invoice_with_line_item
from playwright.sync_api import expect
from uuid import uuid4
import variables

@pytest.mark.regression
def test_customer_validate_accounting_options(page, login, api_request_context):

    # Preconditions: create customer and invoice with line item

    customer = Customer(business_name = 'John' + str(uuid4())[1:10])
    customer.create(api_request_context)

    invoice_id = create_invoice_with_line_item(page, customer.business_name[1:10])

    page.goto(f'{variables.base_url}/customers')

    # Click on 'More Info' tooltipper
    page.click(f'#quick-view-customer-{customer.customer_id}')

    # Verify that quick view form has Accountin options:
    expect(page.locator('div.qv-overview.row')).to_contain_text('balance$300.00credit$0.00total invoiced$300.00 ')

    # Click 'Edit' button
    page.click('div.btn-bar a.btn.btn-default:has-text("Edit")')

    # Verify that we are on the customer edit page
    expect(page.locator('span.customer-title')).to_contain_text('Editing: John')

    expect(page.locator('div#customer-edit-customer-info')).to_contain_text("BASIC INFO")
    expect(page.locator('div#customer-edit-customer-info')).to_contain_text("CUSTOMER SETTINGS")
