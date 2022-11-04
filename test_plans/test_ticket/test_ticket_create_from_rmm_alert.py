import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import Ticket
from helpers.customer import create_customer
from helpers.asset import create_asset
from helpers.rmm_alert import create_rmm_alert
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
def test_ticket_create_from_rmm_alert(page, login, api_request_context):
    # Create customer
    customer_name = 'Customer1'+ str(uuid.uuid4())
    customer_id, _ = create_customer(customer_name, api_request_context)

    # Creaste asset
    asset_id, _, asset_name = create_asset(page, customer_id, api_request_context)
    page.goto(f'{variables.base_url}/customer_assets')

    # Create RMM Alert
    rmm_alert_id = create_rmm_alert(customer_id, asset_id, api_request_context)

    # Go to rmm alerts page
    page.goto(f'{variables.base_url}/rmm_alerts')

    # Click 'Create' ticket from the RMM alert
    page.click('table.table-striped td a:has-text("Create")')

    # Verify that new ticket was created from RMM Alert - it has customer name, asset name and description from RMM Alert

    expect(page.locator('div.widget.borderless.overflowable:has-text("Customer Info")')).to_contain_text('Customer1')

    expect(page.locator('div.widget.overflowable:has-text("RELEVANT ASSETS") a.table-entry-head')).to_contain_text(f'{asset_name[0:10]}')

    expect(page.locator('div.comment-list.pbm')).to_contain_text('New RMM Alert test description')

