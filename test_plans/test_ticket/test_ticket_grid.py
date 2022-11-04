import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import Ticket
from playwright.sync_api import expect
from time import sleep
import variables

@pytest.mark.regression
def test_ticket_grid(page, login, api_request_context):
    # Preconditions: create ticket
    ticket = Ticket()
    ticket.create(api_request_context)

    page.goto(f'{variables.base_url}/tickets')
    expect(page.locator(f'tr.bhv-ticketRow{ticket.ticket_id}')).to_contain_text('Remote Support')

    # Customize ticket table column
    # Hide Issue and show Creator
    page.click('a[href="#ticket-columns"]')
    page.click('div.modal-body span:has-text("Issue")')
    page.click('div.modal-body span:has-text("Timer")')
    page.click('div.modal-body a:has-text("Save")')

    expect(page.locator(f'tr.bhv-ticketRow{ticket.ticket_id}')).not_to_contain_text('Remote Support')
    expect(page.locator(f'tr.bhv-ticketRow{ticket.ticket_id}')).to_contain_text('0:00:00')


    # Bulk Edit Tickets - change Status
    page.click('input.selectall')
    page.click('a#bulk_action_button')
    page.select_option('select#tickets_status', label = 'In Progress')
    page.click('input[value="Send"]')
    # Wait for the modal to send the form and close itself
    sleep(5)
    # Wait for Bulk Edit worker to finish
    page.goto(f'{variables.base_url}/tickets')

    # Resolve the ticket from the index page
    page.hover(f'tr.bhv-ticketRow{ticket.ticket_id}')
    page.click(f'tr.bhv-ticketRow{ticket.ticket_id} a.btn-quick-resolve')
    sleep(2)
    page.goto(f'{variables.base_url}/tickets')
    expect(page.locator('div#bhv-ticketTable')).not_to_contain_text(str(ticket.number))