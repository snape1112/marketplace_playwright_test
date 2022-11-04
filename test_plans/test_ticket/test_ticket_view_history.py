
import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import Ticket
from time import sleep
from playwright.sync_api import expect
import variables

@pytest.mark.regression
def test_ticket_view_history(page, login, api_request_context):
    # Create ticket
    ticket = Ticket()
    ticket.create(api_request_context)

    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}/edit')
    # Change ticket status from New to Invoiced
    page.select_option('select#ticket_status', 'Invoiced')
    page.click('button.bhv-CreateTicket:has-text("Save Changes")')
    # Click View History (Admin only)
    # Wait for JS to change the link behaviour
    sleep(5)
    page.click('a.bhv-loadChangeHistory:has-text("View History")')

    # Verify the record 'status New to Invoiced' appears in the 'Change History' table
    expect(page.locator('div.content-target')).to_contain_text("Change History")
    expect(page.locator('div.content-target')).to_contain_text("status New to Invoiced")
