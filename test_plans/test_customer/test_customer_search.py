import pytest
from fixtures import constants
from fixtures.login import create_account, login
from helpers.customer import Customer
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_customer_search(page, login, api_request_context):

# Preconditions: create customer
# We need to create 3 different object Customer class for customer search test

    customer1 = Customer(first_name = 'John', last_name = 'Smith')
    customer1.create(api_request_context)

    customer2 = Customer(phone='123456789')
    customer2.create(api_request_context)

    customer3 = Customer(first_name = 'Ann',
                        last_name = 'Johnson',
                        business_name = 'AJ MSP Service' + str(uuid.uuid4())[1:10],
                        phone= '222111333')
    customer3.create(api_request_context)

    # Customer search by first_name
    page.goto(f'{variables.base_url}/customers')

    page.fill('input#q_query', 'John')
    page.click('div button.btn.btn-default:has-text("Search")')

    # Verify
    expect(page.locator('div.main-inner')).to_contain_text(customer1.business_name)
    expect(page.locator('div.main-inner')).not_to_contain_text(customer2.business_name)
    expect(page.locator('div.main-inner')).to_contain_text(customer3.business_name)


    # Customer search by email
    page.fill('input#q_query', '@syncromsp.com')
    page.click('div button.btn.btn-default:has-text("Search")')

    # Verify
    expect(page.locator('div.main-inner')).to_contain_text(customer1.business_name)
    expect(page.locator('div.main-inner')).to_contain_text(customer2.business_name)
    expect(page.locator('div.main-inner')).to_contain_text(customer3.business_name)

    # Customer search by phone
    page.fill('input#q_query', '123456789')

    # Verify that a single match redirects to the customer page
    # The single match case also changes the button from "Search" to "Go to Customer"
    # I don't want to wait for the button change
    # So we can select the button by form class insted of the button text
    page.click('form.q button.btn.btn-default')

    # Sometimes Playwright fails to update page.url after a redirect
    # Verify "Overview" widget is present, this means we're on the customer show page
    assert page.locator('div.widget-header:has-text("overview")').inner_text()

    # Verify
    expect(page.locator('div.main-inner')).not_to_contain_text(customer1.business_name)
    expect(page.locator('div.main-inner')).to_contain_text(customer2.business_name)
    expect(page.locator('div.main-inner')).not_to_contain_text(customer3.business_name)



