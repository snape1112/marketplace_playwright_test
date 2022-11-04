import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
from datetime import date
from time import sleep
from helpers.ticket import wait_for_worker
import variables

def run_now(page, r_ticket_name, subject, problem_type, description, frequency):
    # Verify we are on the Recurring Ticket Schedule List
    expect (page.locator('body')).to_contain_text('Recurring Tickets Schedules List')

    # Table with recurring tickets should exist
    assert page.locator('table#datatable') != None

    # On the Recurring Tickets Schedules List page check that a line with recurring ticket name was added
    # and it has the frequency we set for the recurring ticket
    assert frequency in page.locator(f'table#datatable tr:has-text("{r_ticket_name}")').inner_text()

    page.click(f'span.table-entry-head:has-text("{r_ticket_name}")')
    page.click('a:has-text("Run Now")')
    wait_for_worker(page, '.cart-contents')

    # Table with a ticket created by 'Run Now' should exist
    assert page.locator('.cart-contents') != None

    # First link in the table is our new ticket
    # We don't know neither number nor id
    # Just click the first link
    page.click('.cart-contents td a')
    # Check the ticket subject, issue type, desription
    assert page.locator('h3.large').inner_text() == subject
    assert page.locator('span[data-bip-attribute="problem_type"]').inner_text() == problem_type
    # Comment description verification. The description attribute was deleted from the ticket helper
    #assert page.locator('div.row div.col-md-12 p').inner_text() == description

@pytest.mark.regression
def test_ticket_create_recurring(page, login, api_request_context):
    # Prerequisites

    customer_name = str(uuid.uuid4())
    customer_id, _  = create_customer(customer_name, api_request_context)

    # Go to Additional Settings page and mark the Enable Recurring Tickets checkbox
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/settings/tickets')
    page.click('a:has-text("Additional Settings")')
    page.check('input#settings_enable_recurring_tickets')
    page.click('input.btn-success:has-text("Save")')

    ticket_id, ticket_num = create_ticket(customer_id, api_request_context)
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets/{ticket_id}')
    page.once("dialog", lambda dialog: dialog.accept())
    next_run_date = date.today().strftime("%m/%d/%Y")

    ###################
    # Recurring Ticket1
    ###################
    assert page.locator(f'text={ticket_num}') != None
    # Create new recurring ticket by clicking into ticket and click on the Actions button > Make Recurring
    page.click('text=Actions')
    page.click('text=Make Recurring')
    # When you open a modal, you need to wait until it loads the JS
    sleep(2)
    r_ticket1_name = "Recurring Ticket 1 New (13 05) created by Make Recurring"
    subject1 = 'Printer not working'
    problem_type1 = 'Remote Support'
    description1 = "Please fix my printer"
    frequency1 = 'Weekly'

    page.fill(f'#ticket_recurring_schedule_name', r_ticket1_name)
    page.select_option('#ticket_recurring_schedule_frequency', frequency1)

    # Next Run should be chosen from the calendar
    page.evaluate(f'$("#ticket_recurring_schedule_next_run_label").datepicker("setDate", "{next_run_date}" )',)

    page.click('input.btn-success:has-text("Create Recurring Ticket Schedule")')
    # Go to Recurring Tickets, then go to the Recurring Ticket that was created in the prior step,
    # Wait a moment after clicking 'Create..', let the form to be sent from the modal
    # Playwright is not going to wait for the modal form to be sent
    # A new rule: wait after opening or closing a modal
    sleep(2)
    expect (page.locator('body')).to_contain_text(f'{customer_name}')
    # Click the "Back" button
    page.click('a[class="btn btn-sm btn-default"]')

    run_now(page, r_ticket1_name, subject1, problem_type1, description1, frequency1)

    ###################
    # Recurring Ticket2
    ###################

    # Create new recurring ticket by heading to Tickets > View > Recurring Tickets
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    page.click('form#ticket_search_form a:has-text("View")')
    page.click("text=Recurring Tickets")

    page.click('a:has-text("New Recurring Ticket Schedule")')

    r_ticket2_name = "My Reccurring Ticket2"
    subject2 = 'My new subject 2'
    problem_type2 = 'Contract Work'
    description2 = 'My new description 2'
    frequency2 = 'Daily'

    # Enter the customer name
    page.type('input#ticket_recurring_schedule_customer_name', customer_name)
    page.click(f'text=/{customer_name}.*/')

    page.click('text=Create Recurring Ticket')

    page.fill('#ticket_recurring_schedule_name', r_ticket2_name)
    page.select_option('#ticket_recurring_schedule_frequency', frequency2)

    # Next Run should be chosen from the calendar
    page.evaluate(f'$("#ticket_recurring_schedule_next_run_label").datepicker("setDate", "{next_run_date}" )',)


    page.fill('input#ticket_recurring_schedule_ticket_subject', subject2)
    page.select_option('#ticket_recurring_schedule_problem_type', problem_type2)
    page.fill('input#ticket_recurring_schedule_description', description2)

    page.click('input.pull-right:has-text("Create Ticket Recurring Schedule")')

    run_now(page, r_ticket2_name, subject2,  problem_type2, description2, frequency2)