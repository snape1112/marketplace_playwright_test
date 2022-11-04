import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_ticket_create(page, login, api_request_context):

        customer_name = str(uuid.uuid4())
        create_customer(customer_name, api_request_context)

        page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/start')

        page.type('#ticket_customer_name', customer_name, delay = 150) 
        page.click(f'text=/{customer_name[:5]}.*/')
        page.click('text=Create Ticket')
 
        page.fill('#ticket_subject', 'Printer not working')
        page.select_option('#ticket_problem_type', 'Remote Support')
        page.focus('#ticket_comments_attributes_0_body')
        page.fill('#ticket_comments_attributes_0_body','Please fix my printer')

        page.click('#ticket_notify_emails_tagsinput')
        page.click('text=Create Ticket')

        assert page.wait_for_selector('text="New"') != None 

