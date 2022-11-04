import uuid 
import pytest
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import variables
 

@pytest.mark.regression
def test_invoice_add_adhoc_bundle(page: Page, login, api_request_context): 

    # Pre-condition

    customer_name = str(uuid.uuid4())
    create_customer(customer_name, api_request_context)
    create_new_invoice(page, customer_name)

    # Add line item 

    page.click('a:has-text("Add Manual Item")')
    page.wait_for_load_state('domcontentloaded')
    page.select_option('#category_ids', label='Default')
    page.fill('[placeholder="A Short Description"]','test')
    page.fill('#line_item_price' ,  '20.00')
    page.fill('#line_item_cost' ,  '20.00')
    page.click('//*[@id="new_line_form_manual"]/div[4]/div[11]/input')

    # Validate line item was created

    assert page.wait_for_selector('text="Added a line item successfully."')!= None
  
    # Create bundle

    page.click('text=Create Ad-Hoc Bundle')
    page.fill('[placeholder="Name\ of\ the\ bundle"]','test')
    page.fill('[placeholder="Description\ of\ the\ bundle"]','lala')
    page.click('button:has-text(\"Create Adhoc Bundle\")')
    
    with page.expect_navigation():
            page.click('button:has-text(\"Save\")')

    # Validate item was created

    locator = page.locator('//*[text()="Item"]/parent::tr/parent::thead/following-sibling::tbody/tr/th')
    assert locator != None
    assert locator.inner_text() == 'test'




