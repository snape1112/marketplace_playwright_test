import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import create_workflow
from playwright.sync_api import Page, expect
import uuid
import variables

@pytest.mark.regression
def test_ticket_clone_workflow(page, login):
    # Prerequisites
    workflow_name = 'Workflow' + str(uuid.uuid4())
    workflow_id = create_workflow(page, workflow_name)

    # Verify that an original Workflow has first name, last name and ticket subject values
    expect(page.locator('input#customer_details-firstname')).to_have_value('Test First')
    expect(page.locator('input#customer_details-lastname')).to_have_value('Test Last')
    expect(page.locator('input#ticket_details-subject')).to_have_value('Test Ticket Subject')

    # Clone Workflow
    page.goto(f'{variables.base_url}/new_ticket_forms')
    page.click('input[value= "Clone"]')
    page.click('a.btn.btn-primary:has-text("Save Workflow")')

    # Verify that Workflow-Clone and original Workflow first name, last name and ticket subject are equal
    expect(page.locator('input#customer_details-firstname')).to_have_value('Test First')
    expect(page.locator('input#customer_details-lastname')).to_have_value('Test Last')
    expect(page.locator('input#ticket_details-subject')).to_have_value('Test Ticket Subject')

    page.goto(f'{variables.base_url}/new_ticket_forms')

    # Verify that Workflow-Clone has the same name as original Workflow  and has word 'Clone' at the end of name
    expect(page.locator('div.widget-content')).to_contain_text(workflow_name + ' (Clone)')

