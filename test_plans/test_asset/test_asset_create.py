import pytest
from uuid import uuid4
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from playwright.sync_api import Page
import variables

#@pytest.mark.regression
#
#def test_asset_create(page: Page, login, api_request_context):

    # Pre-conditions

    # customer_name = str(uuid4())
    # create_customer(customer_name, api_request_context)

    # # Create new assert

    # page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/asset_types')
    # page.click('text=New Asset Type')
    # page.fill('id=asset_type_name','Computer')
    # page.click('text=Create Asset type')
    # page.click('text=Back to Assets')
    # page.click('text=New Asset New Ticket >> a')
    # page.click('a[href="/customer_assets/new_manual"]')
    # page.select_option('#asset_asset_type_id', label='Computer')
    # page.click('#asset_customer_name')
    # page.type('#asset_customer_name', customer_name)
    # page.click(f'text=/{customer_name[:5]}.*/')
    # page.fill('#asset_name', 'Test Asset')
    # page.fill('#asset_asset_serial', '1')
    # page.click('#createAssetSubmit')

    # # Validate label is shown

    # assert page.wait_for_selector('text=Created')!= None
 


