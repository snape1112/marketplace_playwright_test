import pytest
import uuid
from fixtures.login import create_account, login
from helpers.ticket import create_custom_field
from playwright.sync_api import Page, expect
import variables


@pytest.mark.regression
def test_ticket_custom_field_edit_from_grid(page : Page, login):
    # Create new custom field to disable

    custom_field_name = str(uuid.uuid4())
    create_custom_field(page, custom_field_name)

    # Validate that it is in the grid

    page.locator(f'text={custom_field_name}') != None
    page.click(f'text={custom_field_name}')

    new_name = str(uuid.uuid4())

    page.fill("input[name=\"name\"]", new_name)
    page.keyboard.press('Enter')
    page.locator(f'text={new_name}') != None
 
 