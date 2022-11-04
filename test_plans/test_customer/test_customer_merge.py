import pytest
from fixtures import constants
from helpers.customer import Customer
from fixtures.login import create_account, login
from helpers.ticket import Ticket
from helpers.invoice import create_new_invoice
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
def test_customer_merge(page, login, api_request_context):

    # Preconditions: create 2 customers, 2 invoices, 2 tickets
    customer_1 = Customer(business_name = 'Ben' + str(uuid.uuid4())[1:10])
    customer_1.create(api_request_context)

    customer_2 = Customer(business_name = 'Holly' + str(uuid.uuid4())[1:10])
    customer_2.create(api_request_context)

    ticket_1 = Ticket(customer_id = customer_1.customer_id, status = "Customer Reply", subject = 'Printer not working')
    ticket_1.create(api_request_context)

    ticket_2 = Ticket(customer_id = customer_2.customer_id, status = "In Progress", subject = 'Subject2')
    ticket_2.create(api_request_context)

    invoice_1_id = create_new_invoice(page, customer_1.business_name)
    invoice_2_id = create_new_invoice(page, customer_2.business_name)

    # Go to customer page
    page.goto(f'{variables.base_url}/customers/{customer_1.customer_id}')

    # Click 'Actions' > 'Merge'
    page.click('div.row.mbm a.btn.btn-default:has-text("Actions")')
    page.on("dialog", lambda dialog: dialog.accept())
    page.click('li:has-text("Merge")')

    # Type second customer name to merge customers
    page.type('input#merge-destination-customer', customer_2.business_name[0:5])

    # This autocomplete is tricky, need to wait after input and each key press
    page.wait_for_timeout(2000)
    page.keyboard.press("ArrowDown")
    page.wait_for_timeout(2000)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)

    page.click('input:has-text("Merge Customers")')

    # Verify that customers were Merged
    # Verify that Tickets table on Customer page has tickets records from both customers
    expect(page.locator('div#tickets-overview')).to_contain_text(str(ticket_1.number))
    expect(page.locator('div#tickets-overview')).to_contain_text("Customer Reply")
    expect(page.locator('div#tickets-overview')).to_contain_text("Printer not working")
    expect(page.locator('div#tickets-overview')).to_contain_text(str(ticket_2.number))
    expect(page.locator('div#tickets-overview')).to_contain_text("In Progress")
    expect(page.locator('div#tickets-overview')).to_contain_text("Subject2")
    # Verify that 'Merge compete.' alert apears
    expect(page.locator('div.alert.alert-info')).to_contain_text('Merge complete.')

    # Verify that invoices records from both customers exist on the customer page after merge
    assert page.locator(f'a[href="/invoices/{invoice_1_id}"]')
    assert page.locator(f'a[href="/invoices/{invoice_2_id}"]')
