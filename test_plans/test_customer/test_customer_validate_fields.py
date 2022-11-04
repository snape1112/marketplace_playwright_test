import pytest
from fixtures import constants
from fixtures.login import create_account, login
from helpers.customer import Customer  # import Customer Class
from playwright.sync_api import expect
import re
import uuid
import variables

@pytest.mark.regression
def test_customer_validate_fields(page, login, api_request_context):

    # Preconditions: create customer

    customer = Customer(business_name = 'IService' + str(uuid.uuid4())[1:10],
                        first_name = 'Jack' + str(uuid.uuid4())[1:10],
                        last_name = 'Smith',
                        address = "111 Berry Street PMB 5555",
                        city = 'Seattle',
                        state = "WA, United States",
                        phone = '12343334321'
                        )
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers')


    # Click on 'More Info' tooltipper
    page.click(f'#quick-view-customer-{customer.customer_id}')

    # Verify Customer business_name, first_name, last_name fields
    expect(page.locator('div.qv-title')).to_contain_text(customer.business_name)
    expect(page.locator('div.qv-title')).to_contain_text(customer.first_name)
    expect(page.locator('div.qv-title')).to_contain_text(customer.last_name)

    # Verify Customer Email, Phone, Links, Created, Address fields in the Quick View

    # Verify Customer email field
    expect(page.locator('table.fit.vtop tr:has-text("Email")')).to_contain_text(customer.email)

    # Verify Customer Phone field
    expect(page.locator('table.fit.vtop tr:has-text("Phone")')).to_contain_text('1234-333-4321')

    # Verify Customer Links field
    expect(page.locator('table.fit.vtop tr:has-text("Links")')).to_contain_text('Customer Online Profile')

    # Verify Customer Created field
    date= page.locator('table.fit.vtop tr:has-text("Created") td').inner_text()
    assert re.match(r'\d\d-\d\d-\d\d\d\d', date)

    # Verify Customer Address field
    expect(page.locator('table.fit.vtop tr:has-text("Address")')).to_contain_text(customer.address)
    expect(page.locator('table.fit.vtop tr:has-text("Address")')).to_contain_text(customer.city)
    expect(page.locator('table.fit.vtop tr:has-text("Address")')).to_contain_text(customer.state)
