import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import create_workflow
from playwright.sync_api import Page, expect
import uuid
import variables

def set_workflow_as_default(page, workflow_id):
    # Go to 'More' > 'Admin' > 'Workflows'
    page.click('span:has-text("More")')
    page.click('ul[role="menu"] a:has-text("Admin")')
    page.click('ul#tickCollapse a:has-text("Workflows")')

    # Edit which ticket-workflow will run by default when creating a new ticket

    expect(page.locator(f'span#best_in_place_new_ticket_form_{workflow_id}_default')).to_have_text("Not Default")
    page.click(f'span#best_in_place_new_ticket_form_{workflow_id}_default')

    expect(page.locator(f'span#best_in_place_new_ticket_form_{workflow_id}_default')).to_have_text("Default")
    # Create new ticket
    page.goto(f'{variables.base_url}/tickets/start')

    # Verify that ticket creating with Workflow2
    expect(page.locator('div.row.pbm h1')).to_contain_text('New Ticket - Workflow2')

    expect(page.locator('div.row.pbm h1')).not_to_contain_text('New Ticket - Workflow1')

    page.select_option('select#ticket_problem_type', value='Remote Support')
    page.fill('textarea#ticket_description', 'Ticket with Workflow 2')
    page.click('div.mtm a:has-text("Save")')

    # Verify that ticket was created from Workflow2 and has the same customer name and ticket subject as Workflow2
    expect(page.locator('div.row div.col-sm-12 h3.large')).to_contain_text('Test Ticket Subject')
    expect(page.locator('div.widget.borderless:has-text("Customer Info")')).to_contain_text('Test First Test Last')

def reset_workflow_to_default_values(page, workflow_id):
    page.goto(f'{variables.base_url}/new_ticket_forms/{workflow_id}/edit')

    # Verify that Workflow has values for first name, last name and ticket subject
    expect(page.locator('input#customer_details-firstname')).to_have_value('Test First')
    expect(page.locator('input#customer_details-lastname')).to_have_value('Test Last')
    expect(page.locator('input#ticket_details-subject')).to_have_value('Test Ticket Subject')

    # Click 'Reset to Default' Workflow Customer Details and Ticket Details
    page.click('div.widget-header:has-text("Customer Details") a.btn.btn-widget:has-text("Reset to Default")')
    page.click('div.widget-header:has-text("Ticket Details") a.btn.btn-widget:has-text("Reset to Default")')
    page.click('text=Save Workflow')

    # Verify that Workflow was reset to default values
    expect(page.locator('input#customer_details-firstname')).not_to_have_value('Test First')
    expect(page.locator('input#customer_details-lastname')).not_to_have_value('Test Last')
    expect(page.locator('input#ticket_details-subject')).not_to_have_value('Test Ticket Subject')

@pytest.mark.regression
def test_ticket_default_workflow(page, login):
    # Prerequisites
    workflow_1_name = 'Workflow1' + str(uuid.uuid4())
    workflow_1_id = create_workflow(page, workflow_1_name)

    workflow_2_name = 'Workflow2' + str((uuid.uuid4()))
    workflow_2_id = create_workflow(page, workflow_2_name)

    reset_workflow_to_default_values(page, workflow_1_id)
    set_workflow_as_default(page, workflow_2_id)
