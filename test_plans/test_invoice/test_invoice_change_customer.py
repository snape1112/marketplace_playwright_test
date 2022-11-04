import pytest
import uuid
from fixtures.constants import *
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import variables

@pytest.mark.regression
def test_invoice_change_customer(page: Page, login, api_request_context): 

        # Pre-condition
        customer_name = str(uuid.uuid4())
        create_customer(customer_name, api_request_context)

        second_customer_name = str(uuid.uuid4())
        create_customer(second_customer_name, api_request_context)

        page.click('a[role="button"]:has-text("More")')
        page.click('ul[role=\"menu\"] >> text=Invoices')
        page.click('#new_search >> text=New Invoice')
        page.click('#invoice_customer_name')
        page.type('#invoice_customer_name',customer_name[:5], delay=150)
        page.click(f'text=/{customer_name[:5]}.*/')
        page.click("text=Create Invoice")   
        message = page.wait_for_selector("text=Created successfully")
        assert message != None

        page.click('text="Change Customer"')
        page.click('#invoice_customer_name')
        page.fill('[placeholder="Attach to existing customer.."]', second_customer_name)
        page.click('input:has-text("Change Customer")')
        label = page.wait_for_selector('text="Invoice was successfully updated."')
        assert label != None 
