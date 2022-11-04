import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
def test_customer_more_info_pdf_options(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'John' + str(uuid.uuid4())[1:10])
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers')

    # Click on 'More Info'
    page.click(f'#quick-view-customer-{customer.customer_id}')
    page.click('div.btn-group i.far.fa-file-pdf')

    # Verify that Customer Label item has href to Customer Label pdf
    href = page.locator('div.qv-hover a.menu-default:has-text("Customer Label")').get_attribute('href')
    assert href == f'/customers/{customer.customer_id}.pdf'

    # Verify that Address Label item has href to Address Label pdf
    href= page.locator('div.qv-hover a.menu-default:has-text("Address Label")').get_attribute('href')
    assert href[0:14] == '/labels?labels'
