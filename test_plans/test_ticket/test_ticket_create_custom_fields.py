import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from playwright.sync_api import expect
import variables

@pytest.mark.regression

def test_ticket_create_custom_fields(page, login):

        check_positive_case(page)
        check_negative_case(page)

def check_positive_case(page):

        # Navigate to the custom field section

        page.click('a[role="button"]:has-text("More")')
        page.click('ul[role="menu"] >> text=Admin')
        page.click('text=Ticket Custom Fields')

        # Create new field
        custom_field_name = 'name1' + str(uuid.uuid4())
        page.click('text=New Custom Field Type')
        page.fill('input[placeholder="e.g., Hardware, Recovery or Virus"]', custom_field_name[:10])
        page.wait_for_timeout(3000)
        page.click('input[value="Create Custom Field"]')

        # Validate that it was created successfully
        page.wait_for_timeout(5000)
        expect(page.locator('div.widget.overflowable:has-text("Custom Field Types")')).to_contain_text('name1')
        assert page.locator("text=Created successfully").inner_text() != None

        # Rename ticket custom field type

        page.click('span[data-bip-attribute="name"]')
        page.fill('form.form_in_place input[name="name"]', 'new name')
        page.click('div.widget.overflowable h3:has-text("Custom Field Types")')
        page.wait_for_timeout(3000)
        # Reload ticket types page
        page.goto(f'{variables.base_url}/ticket_types/')

        # Verify that ticket custom field type was renamed
        expect(page.locator('div.widget.overflowable:has-text("Custom Field Types")')).to_contain_text('new name')
        expect(page.locator('div.widget.overflowable:has-text("Custom Field Types")')).not_to_contain_text('name1')

def check_negative_case(page):
        # Navigate to the custom field section

        page.click('a[role="button"]:has-text("More")')
        page.click('ul[role="menu"] >> text=Admin')
        page.click('text=Ticket Custom Fields')

        # Create new field with empty name

        custom_field_name = 'name2'+ str(uuid.uuid4())
        page.click('text=New Custom Field Type')
        page.click('input[value="Create Custom Field"]')

        # Validate that it wasn't created successfully

        page.wait_for_timeout(3000)
        assert page.locator("text=Can't Be Blank").inner_text() != None
        expect(page.locator('div#wrapper')).not_to_contain_text('Created successfully')

