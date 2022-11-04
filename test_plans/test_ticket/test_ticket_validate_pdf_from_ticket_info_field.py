import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
import variables


def test_ticket_validate_pdf_options(page, login, api_request_context):
    customer_name = str(uuid.uuid4())
    customer_id = create_customer(customer_name, api_request_context)
    ticket_id, ticket_num = create_ticket(customer_id,api_request_context)
    quick_view_selector = '#quick-view-ticket-{}'.format(ticket_id)

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    page.wait_for_selector(quick_view_selector)
    page.click(quick_view_selector) 


    options = ["Intake Form", "Large Ticket", "Ticket Receipt", "Ticket Label", "Customer Label"]
    for option in options:
        page.click('a[class="btn btn-default dropdown-toggle "]')
        page.click(f"text={option}")
        page.click(f'{quick_view_selector} div[aria-labelledby="timerModalLabel"] button[data-dismiss="modal"][class="btn btn-default btn-sm"]')
