import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import create_custom_field
import variables
from playwright.sync_api import expect

def create_custom_field_field(page):
        # Navigate to the custom field section
        page.click('a[role="button"]:has-text("More")')
        page.click('ul[role="menu"] >> text=Admin')
        page.click('text=Ticket Custom Fields')

        # Create new field

        custom_field_name = str(uuid.uuid4())
        create_custom_field(page, custom_field_name)

        # Create new field field
        page.click('a[role="button"]:has-text("More")')
        page.click('ul[role="menu"] >> text=Admin')
        page.click("text=Ticket Custom Fields")
        manage_page_anchor = page.locator(f'//*[text()="{custom_field_name}"]//parent::td//following-sibling::td/a').first
        manage_page_anchor.click()

        # Create custom field field

        custom_field_field_name = 'cf_name'+ str(uuid.uuid4())

        page.click('text=New Field')
        page.click('input[name="ticket_field[name]"]')
        page.fill('input[name="ticket_field[name]"]',custom_field_field_name)
        page.once('dialog', lambda dialog: dialog.dismiss())
        page.check('text=Required >> input[name="ticket_field[required]"]')
        with page.expect_navigation():
            page.click("text=Create Ticket field")
        # Validate that it was created successfully
        page.wait_for_timeout(5000)
        expect(page.locator('div.widget:has-text("Fields")')).to_contain_text('cf_name')
        assert page.locator('text=Created successfully').inner_text() != None

def edit_custom_field_field(page):
    expect(page.locator('div.widget-table')).not_to_contain_text('Popup')
    page.click('div.widget-table td a:has-text("Edit")')
    page.select_option('div.form-group select#ticket_field_field_type', label="Popup")
    page.click('div.widget-content input[value="Update Ticket field"]')
    expect(page.locator('div.widget-table')).to_contain_text('Popup')

@pytest.mark.regression
def test_ticket_create_custom_field_field(page, login):
    create_custom_field_field(page)
    edit_custom_field_field(page)


