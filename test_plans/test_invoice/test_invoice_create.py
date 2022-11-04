import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer 
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_invoice_create(page, login, api_request_context):

        # Pre-condition

        customer_name = str(uuid.uuid4())
        create_customer(customer_name, api_request_context)

        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/invoices')
        page.click('#new_search >> text=New Invoice')
        page.click('#invoice_customer_name')
        page.type('#invoice_customer_name', customer_name[:5], delay=150)
        page.click(f'text=/{customer_name[:5]}.*/')
        page.click('text=Create Invoice')   
        assert page.wait_for_selector('text=Created successfully') != None
 