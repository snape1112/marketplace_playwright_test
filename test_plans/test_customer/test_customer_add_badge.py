#https://repairtechsolutions.atlassian.net/browse/QA-633
import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
import variables

@pytest.mark.regression
def test_add_badge(page, login, api_request_context): 

    # Pre-conditions

    customer_name = str(uuid.uuid4())
    create_customer(customer_name, api_request_context)

    # Create badge

    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] a:has-text("Admin")')
    page.click('text=Customer Custom Fields')
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/customer_fields/new')
    page.fill('id=customer_field_name','new')
    page.select_option('id=customer_field_field_type' , label='Drop Down')
    page.click('text=Add Answer')
    page.click('text=Toggle Dropdown')
    page.click('i[class="fab fa-500px"]')
    page.click('text=Create Customer field')

    # Validate label is shown (Should also check for existence)

    assert page.wait_for_selector('text="Created successfully"') != None 
 
