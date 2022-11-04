import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_invoice_with_line_item
import variables
 

@pytest.mark.regression
@pytest.mark.smoke
def test_invoice_payment(page, login, api_request_context):

    # Pre-condition

    customer_name = str(uuid.uuid4()) 
    create_customer(customer_name, api_request_context) 
    create_invoice_with_line_item(page, customer_name) 

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/invoices')
    page.click(f'text=/{customer_name[:5]}.*/')
    page.click('text=Take Payment')
    page.fill('input[name="payment[ref_num]"]', '4111111111111111')
    page.click('text=Take Payment')
    assert page.wait_for_selector('text=× Payment successfully applied') != None
    ref_text_element = page.wait_for_selector('//*[text()="Ref:"]/parent::p') 
    assert ref_text_element.inner_text() == 'Ref: 4111111111111111'
