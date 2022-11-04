import pytest
from uuid import uuid4
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import Ticket
from helpers.asset import create_asset
from playwright.sync_api import Page, expect
import variables

@pytest.mark.regression
def test_ticket_add_remove_asset(page, login, api_request_context):
    # Preconditions: create asset and a ticket
    ticket = Ticket()
    ticket.create(api_request_context)
    _,_, asset_name = create_asset(page, ticket.customer_id, api_request_context)


    # Action: add the asset to the ticket
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')
    # Add Asset
    page.click('text=Add Existing')
    page.click('.btn.btn-default.input-group-addon')
    page.click('div[id^=ui-id-]')
    page.click('//*[text() = "Add"]')
    # Expected result: asset is added
    assert page.locator(f'td:has-text("{asset_name[0:10]}")').inner_text() != None

    # Remove Asset
    page.click('div.btn-group a.btn.btn-xs.btn-sm.dropdown-toggle:has-text("•••")')
    page.click('button.menu-danger:has-text("Remove")')
    expect(page.locator('div.widget.overflowable:has-text("relevant assets")')).not_to_contain_text(asset_name[0:10])
    expect(page.locator('div.widget.overflowable:has-text("relevant assets")')).to_contain_text('There are no relevant assets.')
