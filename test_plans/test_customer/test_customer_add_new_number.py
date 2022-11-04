import pytest
from fixtures import constants
from helpers.customer import create_customer
from fixtures.login import create_account, login
import uuid
import variables

@pytest.mark.regression
def test_customer_add_new_number(page, login, api_request_context):

    # Preconditions: create customer
    customer_name = 'John' + str(uuid.uuid4())[1:10]
    customer_id, _ = create_customer(customer_name, api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer_id}')


    page.click("text=Edit")

    page.click("text=Add New Number")

    page.locator("xpath=//input[@id='customer_phones_attributes_0_number']").fill("5555554555")

    page.click("text=Save Changes")

    assert page.wait_for_selector('text="Customer successfully updated."') != None 