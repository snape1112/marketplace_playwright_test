#https://repairtechsolutions.atlassian.net/browse/QA-1373
import uuid 
import pytest
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import variables

@pytest.mark.regression
def test_invoice_add_manual_line_item(page:Page, login, api_request_context):

    # Pre-condition

    customer_name = str(uuid.uuid4()) 
    create_customer(customer_name, api_request_context)
    create_new_invoice(page, customer_name)

    # Create line item

    page.click('a:has-text("Add Manual Item")')
    page.wait_for_load_state('domcontentloaded')
    page.select_option('#category_ids', label='Default')
    page.fill('[placeholder="A Short Description"]','test')
    page.fill('#line_item_price' ,  '20.00')
    page.fill('#line_item_cost' ,  '20.00')
    page.click('//*[@id="new_line_form_manual"]/div[4]/div[11]/input')

    # Validate items was added and label was shown

    assert page.wait_for_selector('text="Added a line item successfully."') != None 

    locator = page.locator('//*[text()="Default"]//parent::tr/td/span/span/p')
    assert locator != None
    assert locator.inner_text() == 'test'
 

 