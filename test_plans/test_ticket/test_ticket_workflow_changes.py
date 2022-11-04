from time import sleep
import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import create_workflow 
from playwright.sync_api import Page, expect
import variables

@pytest.mark.regression
def test_ticket_workflow_changes(page, login):
    # Prerequisites
    workflow_name = 'Test Workflow'
    workflow_id = create_workflow(page, workflow_name)

    # Testing
    # Open the new workflow
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/new_ticket_forms/{workflow_id}/edit')

    # Add 2 sections
    page.click('text="Add Section"')
    page.click('text="Ticket Charges"')
    expect (page.locator('dev.widget-header:has-text("Ticket Charges")'))

    page.click('text="Add Section"')
    page.click('text="Assets"')
    expect (page.locator('dev.widget-header:has-text("Related Assets")'))

    # Move Section
    # Positioning Setup
    section_3_header = '//*[@id="wrapper"]/div[3]/div/div/div[4]/div/div[1]/div/div/div[2]/div[3]/div[1]/h3'
    section_4_header = '//*[@id="wrapper"]/div[3]/div/div/div[4]/div/div[1]/div/div/div[2]/div[4]/div[1]/h3'
    section_3_down_button = '//*[@id="wrapper"]/div[3]/div/div/div[4]/div/div[1]/div/div/div[2]/div[3]/div[1]/div/span/span/a[2]'
    section_4_up_button = '//*[@id="wrapper"]/div[3]/div/div/div[4]/div/div[1]/div/div/div[2]/div[4]/div[1]/div/span/span/a[1]'
    
    # Movement
    page.click(section_4_up_button)
    expect(page.locator(section_3_header)).to_contain_text('Related Assets')
    expect(page.locator(section_4_header)).to_contain_text('Ticket Charges')

    page.click(section_3_down_button)
    expect(page.locator(section_3_header)).to_contain_text('Ticket Charges')
    expect(page.locator(section_4_header)).to_contain_text('Related Assets')
    
    # Collapse Section
    expect(page.locator('text="Additional Emails to notify for comments"')).to_be_visible
    page.click('//*[text()="Ticket Details"]//parent::div/div/span/a[3]/i')
    expect(page.locator('text="Additional Emails to notify for comments"')).to_be_hidden
    # 'parent::div' is used because "Ticket Charges" is a <h3> entry inside the div.  
    # You need to move from <h3> to the parent div in order to access the children of that div

    # Expand Section
    page.click('//*[text()="Ticket Details"]//parent::div/div/span/a[3]/i')
    expect(page.locator('text="Additional Emails to notify for comments"')).to_be_visible

    # Remove a Section
    page.click('//*[text()="Ticket Charges"]//parent::div/div/span/a')
    expect(page.locator('text="Ticket Charges"')).not_to_be_visible   