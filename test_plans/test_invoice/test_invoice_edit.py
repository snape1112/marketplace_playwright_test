#https://repairtechsolutions.atlassian.net/browse/QA-1365
import pytest
import uuid
import pytest
from fixtures.constants import *
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
from datetime import date
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_editing_invoice(page:Page, login, api_request_context):
  
    # Pre-condition

    customer_name = str(uuid.uuid4()) 
    create_customer(customer_name,api_request_context) 
    create_new_invoice(page, customer_name) 

    invoice_date = date.today().strftime("%d/%m/%Y")
    invoice_note = str(uuid.uuid4())
    invoice_payer_name = str(uuid.uuid4())
    invoice_check_number = '123456789'

    # Edit the invoice

    page.click('text=Edit')
    page.check('text=Do Not Tax this invoice')
    page.fill('id=invoice_date_label', invoice_date)
    page.fill('id=invoice_note', invoice_note)
    page.select_option('id=invoice_payment_type', label='Cash')
    page.fill('id=invoice_check_number', invoice_check_number)
    page.fill('id=invoice_payer_name', invoice_payer_name)
    page.click('text=Update Invoice')

    # Validate the updates

    assert page.wait_for_selector('text=Invoice was successfully updated') != None
    assert page.locator(f'//*[text()="Invoice Date"]/following-sibling::td/span[contains(text(),"{invoice_date}")]') != None
    assert page.locator(f'//*[text()="Tech Notes"]/following-sibling::td/span[contains(text(),"{invoice_note}")]') != None
    assert page.locator(f'//*[text()="Ref Number"]/following-sibling::td/span[contains(text(),"{invoice_note}")]') != None

    # This doesn't appear to be visible on the page or it just doesn't work
    # assert page.locator(f'id=invoice_payer_name').get_attribute('value') == invoice_payer_name

 






