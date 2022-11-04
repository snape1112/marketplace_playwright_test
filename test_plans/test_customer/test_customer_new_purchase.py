import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer_purchase import create_customer_purchase
from helpers.customer import Customer
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
def test_customer_new_purchase(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'John' + str(uuid.uuid4())[1:10], first_name = 'John', last_name = 'Smith')
    customer.create(api_request_context)
    customer_purchase_id = create_customer_purchase(page, customer.business_name)

    # Delete Customer Purchase

    page.goto(f'{variables.base_url}/customer_purchases')
    page.on("dialog", lambda dialog: dialog.accept())
    # Click 'Delete'
    page.click(f'a[data-method="delete"][href="/customer_purchases/{customer_purchase_id}"]')
    # Verify that Customer Purchase was deleted
    expect(page.locator('table.table-striped.borderless')).not_to_contain_text(customer.business_name)

