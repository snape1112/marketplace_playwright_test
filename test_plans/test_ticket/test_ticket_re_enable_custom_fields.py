import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import create_custom_field
from playwright.sync_api import Page, expect
import variables


@pytest.mark.regression
def test_ticket_disable_custom_fields(page, login):

    # Create new custom field to disable

    custom_field_name = str(uuid.uuid4())
    create_custom_field(page, custom_field_name)

    # Validate that it is in the grid

    page.locator(f'text={custom_field_name}') != None

    # Disable

    page.once('dialog', lambda dialog: dialog.accept())
    page.click(f'//*[text()="{custom_field_name}"]/parent::td/parent::tr/td[3]/a')
 
    # Validate that it is in the disabled list
    
    expect(page.locator('//*[text()="Disabled Custom Field Types"]//ancestor::div[1]//following-sibling::div//child::tbody//child::td[1]').first).to_contain_text(custom_field_name)

    # Re-enable it
    page.click(f'//*[text()="{custom_field_name}"]/parent::tr/td[2]')


    expect(page.locator('//*[text()="Custom Field Types"]//ancestor::div[1]//following-sibling::div//child::tbody//child::td[1]').first).to_contain_text(custom_field_name)


 