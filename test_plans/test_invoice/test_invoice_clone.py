import uuid 
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import pytest
import variables

@pytest.mark.regression
def test_clone_invoice(page:Page, login, api_request_context):

    # Pre-condition

    customer_name = str(uuid.uuid4()) 
    create_customer(customer_name, api_request_context) 
    create_new_invoice(page, customer_name)

    page.click('text=actions')
    page.click('text=delete')