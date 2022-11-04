import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer_purchase import create_customer_purchase, set_customer_purchase_status, add_manual_item_to_customer_purchase
from helpers.customer import Customer
from playwright.sync_api import expect
import re
import uuid
import variables
from datetime import date

@pytest.mark.regression
def test_customer_purchase_validate_fields(page, login, api_request_context):

    # Preconditions: create customer and customer purchase
    customer = Customer(business_name = 'John' + str(uuid.uuid4())[1:10], last_name = 'Smith')
    customer.create(api_request_context)

    customer_purchase_id = create_customer_purchase(page, customer.business_name)

    # Add Item to the Purchase (Manual New Inventory Item)
    add_manual_item_to_customer_purchase(page)

    page.goto(f'{variables.base_url}/customer_purchases')

    # Validate customer business name field
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer.business_name)

    # Validate Item field
    expect(page.locator('table.table-striped.borderless tbody tr> td >> nth=0')).to_have_text('Acer:')

    # Verify Amount field
    expect(page.locator('table.table-striped.borderless tbody tr> td >> nth=1')).to_have_text('$200.00')

    # Validate Status field
    expect(page.locator('table.table-striped.borderless tbody tr> td >> nth=2')).to_have_text('Paid')

    # Validate Paid field
    assert 'Paid' in page.locator('table.table-striped.borderless tbody tr> td >> nth=3').inner_html()

    # Validate 'Created' field
    date = page.locator('table.table-striped.borderless tbody tr> td >> nth=4').inner_text()
    assert re.match(r'\D\D\D \d\d-\d\d-\d\d \d\d:\d\d\ \D\D', date)
