import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
import uuid
from playwright.sync_api import expect
import variables

@pytest.mark.regression
def test_customer_validate_pdf_options(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'IService' + str(uuid.uuid4()), first_name = 'John', last_name = 'Smith')
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')

    page.click('div.btn-group i.far.fa-file-pdf')

    # Verify that Customer Label item has href to Customer Label pdf
    href = page.locator('ul.dropdown-menu a.menu-default:has-text("Customer Label")').get_attribute('href')
    assert href == f'/customers/{customer.customer_id}.pdf'

    # Verify that Address Label item has href to Address Label pdf
    href= page.locator('ul.dropdown-menu a.menu-default:has-text("Address Label")').get_attribute('href')
    assert href[0:14] == '/labels?labels'
