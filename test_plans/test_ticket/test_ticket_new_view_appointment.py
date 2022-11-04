import pytest
from uuid import uuid4
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
from helpers.ticket import Ticket
from helpers.appointment import validate_appointment
import variables

@pytest.mark.regression
def test_new_view_appointment(page, login, api_request_context):
    # Prerequisites
    customer = Customer(business_name = 'IService' + str(uuid4()))
    customer.create(api_request_context)

    ticket = Ticket(customer_id = customer.customer_id)
    ticket.create(api_request_context)

    # Go to the ticket page
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')
    validate_appointment(page, customer.business_name, 'Remote Support', 'Morning of and 1 hour before')

