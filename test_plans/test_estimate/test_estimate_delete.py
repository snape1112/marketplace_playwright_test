import uuid 
import pytest
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.estimate import create_estimate
import re
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_deleting_estimate(page : Page, login, api_request_context):

    # Pre-condition
    
    customer_name = str(uuid.uuid4()) 
    create_customer(customer_name, api_request_context) 
    create_estimate(page, customer_name)  
    page.once("dialog", lambda dialog: dialog.accept())

    # Delete estimate

    estimate_value = page.locator('text=/Estimate #(\d+)/').inner_text()
    estimate_number_result = re.search(r"(\d+)", estimate_value)
    estimate_number = estimate_number_result.group(0)
    page.click('text=actions')
    page.click('text=delete')

    # Validate that it is removed

    assert page.wait_for_selector(f'text=We deleted # {estimate_number}') != None
    assert page.locator(f'text=/{estimate_number}/') != None
 
