import pytest
from fixtures import constants
from helpers.customer import Customer
from fixtures.login import create_account, login
from helpers.ticket import Ticket
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_customer_delete(page, login, api_request_context):

    # Preconditions: create 2 customers, the first customer has no tickets, the second customer has ticket

    customer_1 = Customer(business_name = 'John' + str(uuid.uuid4())[1:10])
    customer_1.create(api_request_context)

    # Create customer 2 which has ticket
    customer_2 = Customer(business_name = 'Ben' + str(uuid.uuid4())[1:10])
    customer_2.create(api_request_context)
    ticket = Ticket(customer_id = customer_2.customer_id )
    ticket.create(api_request_context)
    page.goto(f'{variables.base_url}/customers')

    # Test case 1
    # Expect Customer which has no tickets was deleted from the system after click on 'Delete'
    page.goto(f'{variables.base_url}/customers/{customer_1.customer_id}')
    page.click('div.row.mbm a.btn.btn-default:has-text("Actions")')
    page.on("dialog", lambda dialog: dialog.accept())
    page.wait_for_timeout(3000) # Let the Flash messages to clear
    # Click 'Delete'
    page.click('li:has-text("Delete")')

    # Verify that Customer 1 was deleted

    expect(page.locator('div.error-container-thingy')).to_contain_text('Customer was deleted from the system.')
    expect(page.locator('table.table-striped.borderless')).not_to_contain_text(str(customer_1.business_name))
    expect(page.locator('table.table-striped.borderless')).to_contain_text(str(customer_2.business_name))

    # Go to customer 2 page
    page.goto(f'{variables.base_url}/customers/{customer_1.customer_id}')
    # Verify that customer 1 page was not found
    assert page.wait_for_selector("text='We didn't find the page you were looking for'")

    # Test case 2
    # Expect Customer was archived instead of deleted because it has ticket
    page.goto(f'{variables.base_url}/customers/{customer_2.customer_id}')
    page.click('div.row.mbm a.btn.btn-default:has-text("Actions")')
    page.on("dialog", lambda dialog: dialog.accept())
    page.wait_for_timeout(3000) # Let the Flash messages to clear
    page.click('li:has-text("Delete")')

    # Verify that Customer was archived instead of deleted
    expect(page.locator('div.error-container-thingy')).to_contain_text('Customer was disabled instead of deleted because they have associated data.')

    expect(page.locator('div.main')).not_to_contain_text("Ben")
    expect(page.locator('div.main')).not_to_contain_text("John")
    # Go to Customer 2 page
    page.goto(f'{variables.base_url}/customers/{customer_2.customer_id}')

    expect(page.locator('div.alert.alert-danger')).to_contain_text('Customer is Archived')
