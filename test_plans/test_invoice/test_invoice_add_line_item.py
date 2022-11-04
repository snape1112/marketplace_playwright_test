import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import variables

@pytest.mark.regression
def test_invoice_add_line_item(page, login, api_request_context):

        # Pre-condition

        customer_name = str(uuid.uuid4()) 
        create_customer(customer_name, api_request_context)
        create_new_invoice(page, customer_name)
        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/invoices')

        # Create the line item

        page.click(f"text=/{customer_name[:5]}.*/")
        page.type('#line_item_item','Labor', delay=150)
        page.click('text="Labor - Labor"')   
        page.click('text=Create Line item')
        page.click('[data-bip-attribute=price]')
        page.fill('input[name="price"]', "300")
        with page.expect_navigation():
                page.click('input:has-text("Save")')

        # Validate the value is set
                
        assert page.wait_for_selector('#line_items_table >> text=$300.00')!= None
 

