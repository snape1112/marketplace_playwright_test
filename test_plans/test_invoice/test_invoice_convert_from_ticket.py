import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket 
import variables

@pytest.mark.regression
def test_invoice_convert_from_ticket(page, login, api_request_context):

        # Pre-conditions

        customer_name = str(uuid.uuid4())
        customer_id, _ = create_customer(customer_name, api_request_context)
        ticket_id, ticket_num = create_ticket(customer_id, api_request_context)

        # Convert ticket

        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
        page.click(f'text={ticket_num}')
        page.click('text=Make Invoice')

        # Validate

        message = page.wait_for_selector('text="Take Payment"')
        assert message != None
