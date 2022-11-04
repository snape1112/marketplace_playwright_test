import uuid
import pytest
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import variables

@pytest.mark.regression

def test_invoice_recurring(page:Page, login,api_request_context): 

    # Pre-condition

    customer_name = str(uuid.uuid4())
    create_customer(customer_name, api_request_context)
    create_new_invoice(page, customer_name)

    # Create recurring invoice

    page.click("text=Actions")
    page.click("text=Make Recurring")
    page.fill('#schedule_generated_invoice_name','test')
    page.select_option('#schedule_frequency', label='Daily')
    page.click('text=Create Schedule')

    # Validate that it was created successfully

    assert page.wait_for_selector('text=Great, now add some line items and you are all set!') != None

