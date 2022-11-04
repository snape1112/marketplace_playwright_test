import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.customer import Customer  # import Customer Class
from playwright.sync_api import expect
import variables
import re
import uuid

def test_customer_grid_fields_accuracy(page, login, api_request_context):

    customer = Customer(business_name = 'IService' + str(uuid.uuid4())[1:10],
                        last_name = 'Smith'
                        )
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers')

    # Validation business name field accuracy
    expect(page.locator('table.table-striped.borderless tbody tr> td >> nth=1')).to_contain_text(customer.business_name)

    # Validate 'Contacts' field
    expect(page.locator('table.table-striped.borderless tbody tr> td >> nth=2')).to_contain_text('0')

    # TODO After Customer class Merge we will be able to verify customer address and customer email
    # Validate 'Email' field
    expect(page.locator('table.table-striped.borderless tbody tr> td >> nth=3')).to_contain_text('@syncromsp.com')

    # Validate 'Phone' field
    expect(page.locator('table.table-striped.borderless tbody tr> td >> nth=4')).to_contain_text('Phone 1425-654-5665')

    # Validate 'Created' field
    date = page.locator('table.table-striped.borderless tbody tr> td >> nth=5').inner_text()
    assert re.match(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) \d\d-\d\d-\d\d \d\d:\d\d\ \w\w', date, re.IGNORECASE)
