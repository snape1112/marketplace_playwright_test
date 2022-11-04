import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from time import sleep
from helpers.ticket import Ticket
import variables

@pytest.mark.regression
def test_ticket_add_labor_log(page, login: login, api_request_context):
    # Create new ticket
    ticket = Ticket()
    ticket.create(api_request_context)

    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')
    # Add ticket timer from the ticket comment form (Communications)
    page.click('div.comment_body textarea#comment_body')
    page.type('div.comment_body textarea#comment_body', 'My new comment')

    page.fill('input#comment_minutes_spent', '30')
    page.check('#comment_bill_time_now')
    page.click('form#new_comment a.bhv-submitComment')

    # Add ticket timer by clicking "play" button on the Labor Log table
    page.fill('input#stopwatch_notes', 'watch')
    page.click('#watch-play')
    page.click('#watch-stop')
    page.click('a:has-text("View Log")')

    # Add ticket timer by using manual ticket timer entry
    # We need to wait for best_in_place
    sleep(5)
    page.click('span[data-bip-attribute="duration"]')
    page.fill('form.form_in_place input[name="duration"]', '15')
    page.click('form.form_in_place input[value="Save"]')
    page.click('a:has-text("Charge Time")')

    page.fill('textarea#manual_time_entry_notes', 'New ticket timer log note')
    page.click('form.manual_time_entry input[name="commit"][value="Add"]')
    page.click('a:has-text("Charge Time")')

    sleep(2)
    page.click('div.modal-header:has-text("Ticket Timer Log") button.close i')

    page.click('a:has-text("Add/View Charges:")')

    comment_quantity = page.locator('tr:has-text("My new comment") span[data-bip-attribute="quantity"]').inner_text()
    assert comment_quantity == "0.5"

    quantity = page.locator('tr:has-text("watch") span[data-bip-attribute="quantity"]').inner_text()
    assert quantity == "0.25"

    default_quantity = page.locator('tr:has-text("New ticket timer log note") span[data-bip-attribute="quantity"]').inner_text()
    assert default_quantity == "1.0"
