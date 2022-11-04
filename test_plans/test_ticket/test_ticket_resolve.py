import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import Ticket
import variables

@pytest.mark.regression
@pytest.mark.smoke
def test_ticket_resolve(page, login, api_request_context):
    # Preconditions: create ticket
    ticket = Ticket()
    ticket.create(api_request_context)

    # Go to the ticket page
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')
    assert page.locator(f'span#best_in_place_ticket_{ticket.ticket_id}_status').inner_text() != 'Resolved'
    page.click('a.dropdown-toggle:has-text("Actions")')

    # Click 'Actions' > 'Resolve' ticket
    page.click('ul.dropdown-menu button.menu-default:has-text("Resolve")')
    # Verify ticket status is Resolved
    assert page.locator(f'span#best_in_place_ticket_{ticket.ticket_id}_status').inner_text() == 'Resolved'

    # Change ticket status to 'New'
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}/edit')
    page.select_option('select#ticket_status', label = 'New')
    page.click('button.bhv-CreateTicket:has-text("Save Changes")')
    assert page.locator(f'span#best_in_place_ticket_{ticket.ticket_id}_status').inner_text() == 'New'

    # Click 'Actions' > 'Quick Resolve' ticket
    page.click('a.dropdown-toggle:has-text("Actions")')
    page.click('ul.dropdown-menu button.menu-default:has-text("Quick Resolve")')
    # Go back to the ticket page
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')

    # Verify ticket status is Resolved
    assert page.locator(f'span#best_in_place_ticket_{ticket.ticket_id}_status').inner_text() == 'Resolved'