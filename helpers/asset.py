import pytest
import re
from uuid import uuid4
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import Page, expect
import variables

def create_asset(page, customer_id, api_request_context):
    """
        Creates asset

        Returns:
            Creates the new asset with the given name and returns asset_id, asset_type, customer_name, asset_name
    """

    #Taking id of the asset_type
    page.goto(f'{variables.base_url}/asset_types')
    asset_type_id = page.locator('span[id^=best_in_place_asset_type_]').first
    parsed_asset_type = re.search(r'(\d+)', asset_type_id.get_attribute('id'))
    asset_type_id = parsed_asset_type.group(0)

    #API call to create an asset
    response = api_request_context.post(
        f'{variables.base_url}/api/v1/customer_assets',
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": variables.token,
        },
    data={
        "asset_type_name": str(uuid4()),
        "asset_type_id": f'{asset_type_id}',
        "properties": {},
        "name": str(uuid4()),
        "customer_id": f'{customer_id}',
        "asset_serial": str(uuid4())
    }
    )
    assert response.ok
    json = response.json()
    asset_id = json['asset']['id']
    asset_type = json['asset']['asset_type']
    asset_name = json['asset']['name']
    return asset_id, asset_type, asset_name
    """potentionaly we can return any value from the response, and the response is including all info about asset, customer,
     portal user url, tax_rate_id, business and full name, rmm_links, rmm data like alerts, AV, etc."""

def create_manual_asset(page, customer_id, **kwargs):
    asset_type_name = kwargs.get('asset_type_name')
    name = kwargs.get('name')
    asset_serial = kwargs.get('asset_serial')
    page.goto(f'{variables.base_url}/customers/{customer_id}')
    page.click('div.widget-header:has-text("Assets") a:has-text("New")')
    page.click('a.menu-default:has-text("Manual Asset")')
    page.select_option('select#asset_asset_type_id', label= asset_type_name)
    page.type('input#asset_name', name)
    page.type('input#asset_asset_serial', asset_serial)
    page.wait_for_timeout(2000)
    page.click('a#createAssetSubmit')
    expect(page.locator('div.alert-info')).to_contain_text('Created')
