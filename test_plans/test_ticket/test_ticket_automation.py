import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import Ticket, wait_for_worker
from playwright.sync_api import expect
import variables

@pytest.mark.regression
def test_ticket_automation(page, login, api_request_context):
    ticket = Ticket(subject = 'Remote printer not working')
    ticket.create(api_request_context)

    # Go to Ticket Automation page
    page.click('span:has-text("More")')
    page.click('ul[role="menu"] a:has-text("Admin")')
    page.click('ul#tickCollapse li:has-text("Ticket Automations")')
    page.click('a.btn-sm:has-text("New Ticket Automation")')

    # Verify that we have 'New Ticket Automation' text on the page
    expect(page.locator('div.col-md-6 h1')).to_contain_text('New Ticket Automation')

    # Fill in the Automation Name
    page.fill('input#automation_name', 'My New Automation')

    # Under the Conditions section, click the + button
    page.click('div.widget-content:has-text("Add New Condition") i.fas.fa-plus')

    # Run the following actions for the matching tickets
    page.select_option('select[name="ticket_automation[conditions_attributes][][condition_type_id]"]', label='Ticket Subject')
    page.fill('input[name="ticket_automation[conditions_attributes][][value]"]', 'Remote printer not working')

    page.click('div.widget-content div div.row:has-text("Add New Action") i.fas.fa-plus')

    page.select_option('select[name="ticket_automation[actions_attributes][][action_type_id]"]', label='Add Public Comment')
    page.fill('textarea[name="ticket_automation[actions_attributes][][body]"]', 'My new comment body')

    page.click('button.btn-success:has-text("Save")')

    # Click 'Run Now' to immediately run Automation
    page.click('input[value="Run Now"]')

    # Go to ticket page
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')


    wait_for_worker(page, 'div.comment-list:has-text("Automation My New Automation ran")')

    # Verification
    comment_text = 'Automation My New Automation ran on this ticket. Actions: Add Public Comment'
    expect(page.locator('div.comment-list')).to_contain_text("My new comment body")
    expect(page.locator('div.comment-list')).to_contain_text("Ticket Automation")
    expect(page.locator('div.comment-list')).to_contain_text(comment_text)
