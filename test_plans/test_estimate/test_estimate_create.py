from uuid import uuid4
import pytest
import re
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_estimate_create(page, login, api_request_context):

    customer_name = str(uuid4())
    create_customer(customer_name, api_request_context)

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/estimates')
    page.locator('a:has-text("New Estimate")').nth(1).click()
    page.click('#estimate_customer_name')
    page.type('#estimate_customer_name', customer_name[:5], delay=150)
    page.click(f'text=/{customer_name[:5]}.*/')
    page.click('text=Create estimate')
    assert page.wait_for_selector('text=Created successfully') != None


        


 