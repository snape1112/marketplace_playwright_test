import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from playwright.sync_api import Page
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_create_customer(page : Page, login: login):

        # Create customer

        customer_name = str(uuid.uuid4())
        page.goto(f'{variables.base_url}/customers/new')
        page.fill('#customer_firstname', str(uuid.uuid4()))
        page.fill('#customer_lastname', str(uuid.uuid4()))
        page.fill('#customer_business_name', customer_name)
        page.fill('#customer_email', str(uuid.uuid4()) + '@syncromsp.com')
        page.click('.address-autocomplete-search')
        page.keyboard.type('test', delay=150)
        page.click('.suggestion-item')
        page.fill('#customer_address_2', str(uuid.uuid4()))
        page.fill('#customer_city', str(uuid.uuid4()))
        page.fill('#customer_state', 'CA')
        page.fill('#customer_zip', '92111')
        page.click('#customer_create_button') 

        # Validate label is shown (Should also check for existence)

        assert page.wait_for_selector('text="Customer was successfully created."') != None 
   