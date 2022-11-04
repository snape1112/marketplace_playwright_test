import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket, create_custom_field
from playwright.sync_api import Page, expect
from helpers.user import user_create
import variables
import datetime
from datetime import timedelta

@pytest.mark.regression
@pytest.mark.smoke
def test_ticket_edit(page, login, api_request_context):

    # Preconditions: creating a user, customer, and a ticket
    customer_name = str(uuid.uuid4())
    user_id, user_name,*_= user_create(page)
    customer_id = create_customer(customer_name, api_request_context)
    ticket_id, ticket_num = create_ticket(customer_id,api_request_context)

    # Preconditions: new items for editing
    round_time = lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 15*(dt.minute // 15))
    new_subject = 'First Edition'
    new_due_date = datetime.datetime.now() + timedelta(days=100)
    new_due_date = round_time(new_due_date)
    new_created_date = datetime.datetime.now()
    new_created_date = round_time(new_created_date)
    new_email = "test@gmail.com"

    # Testing the editing functionality
    create_ticket(customer_id, api_request_context)
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}')
    page.click('text=Edit')
    page.fill('#ticket_subject', new_subject)
    page.select_option('//*[@id="ticket_status"]', 'In Progress')
    # Time and date picker 
    page.evaluate(f'$("#ticket_due_date_label").datepicker( "setDate", "{new_due_date}" )',)
    page.evaluate(f'$("#ticket_created_at_label").datepicker( "setDate", "{new_created_date}" )',)

    page.select_option('#ticket_problem_type', "Contract Work")
    page.type('#ticket_notify_emails_tag', new_email)
    page.keyboard.press("Enter")
    page.select_option('#ticket_user_id', user_id)
    page.check('#ticket_cancelled')
    page.click("text=Save Changes")    

    #Assertions for all the edited fields
    expect(page.locator('.large')).to_have_text(new_subject)
    expect(page.locator(f'#best_in_place_ticket_{ticket_id}_status')).to_have_text('In Progress')
    expect(page.locator(f'#best_in_place_ticket_{ticket_id}_problem_type')).to_have_text('Contract Work')
    assert page.locator('//*[text()="Due Date"]/following-sibling::td/span').inner_text().upper() == new_due_date.strftime("%b %#d %#I:%M%p").upper()
    assert page.locator('//*[text()="Created"]/following-sibling::td/span').inner_text().upper() == new_created_date.strftime("%a %#I:%M%p").upper()
    expect(page.locator(f'#best_in_place_ticket_{ticket_id}_user_id')).to_have_text(user_name)
