import uuid 
import pytest
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import re
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_deleting_invoice(page : Page, login,api_request_context):

    # Pre-condition
    
    customer_name = str(uuid.uuid4()) 
    create_customer(customer_name, api_request_context) 
    create_new_invoice(page, customer_name)  
    page.once("dialog", lambda dialog: dialog.accept())

    # Delete invoice

    invoice_value = page.locator('text=/Invoice #(\d+)/').inner_text()
    invoice_number_result = re.search(r"(\d+)", invoice_value)
    invoice_number = invoice_number_result.group(0)
    page.click('text=actions')
    page.click('text=delete')

    # Validate that it is removed

    assert page.wait_for_selector(f'text=We deleted # {invoice_number}') != None
    assert page.locator(f'text=/{invoice_number}/') != None
 


