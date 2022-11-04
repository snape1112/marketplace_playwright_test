import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer_purchase import create_customer_purchase, set_customer_purchase_status
from helpers.customer import Customer
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
def test_customer_purchase_search(page, login, api_request_context):

    # Preconditions: create 2 customers and 2 customer purchases for search
    customer1 = Customer(business_name = 'John' + str(uuid.uuid4())[1:10], last_name = 'Smith')
    customer1.create(api_request_context)

    customer_purchase1_id = create_customer_purchase(page, customer1.business_name)

    # Change Customer Purchase status for Search by Status
    set_customer_purchase_status(page, 'Paid')

    customer2 = Customer(business_name = 'Dave' + str(uuid.uuid4())[1:10], last_name = 'Davidson')
    customer2.create(api_request_context)

    # Enable_setting flag let me skip Customer Purchase setting
    # When I call the method multiple times in the same test
    customer_purchase2_id = create_customer_purchase(page, customer2.business_name, enable_setting=False)

    page.goto(f'{variables.base_url}/customer_purchases')

    # Customer Purchase Seatch by Status 'Paid'
    page.select_option('select#q_status_eq', 'Paid')
    page.click('input[value="Search"]')
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer1.business_name)
    expect(page.locator('table.table-striped.borderless')).not_to_contain_text(customer2.business_name)


    # Customer Purchase Seatch by Status 'Estimate'
    page.select_option('select#q_status_eq', 'Estimate')
    page.click('input[value="Search"]')
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer2.business_name)
    expect(page.locator('table.table-striped.borderless')).not_to_contain_text(customer1.business_name)

    # Clear the Status filter
    page.select_option('select#q_status_eq', '')
    page.click('input[value="Search"]')
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer2.business_name)
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer1.business_name)

    # Customer Purchase Search by customer1 business name
    page.fill('input#q_notes_cont', customer1.business_name)
    page.click('input[value="Search"]')
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer1.business_name)
    expect(page.locator('table.table-striped.borderless')).not_to_contain_text(customer2.business_name)

    # Customer Purchase Search by customer2 business name
    page.fill('input#q_notes_cont', customer2.business_name)
    page.click('input[value="Search"]')
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer2.business_name)
    expect(page.locator('table.table-striped.borderless')).not_to_contain_text(customer1.business_name)

    # Customer Purchase Search by customer1 last name
    page.fill('input#q_notes_cont', customer1.last_name)
    page.click('input[value="Search"]')
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer1.business_name)
    expect(page.locator('table.table-striped.borderless')).not_to_contain_text(customer2.business_name)

    # Customer Purchase Search by customer2 last name
    page.fill('input#q_notes_cont', customer1.last_name)
    page.click('input[value="Search"]')
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer1.business_name)
    expect(page.locator('table.table-striped.borderless')).not_to_contain_text(customer2.business_name)

