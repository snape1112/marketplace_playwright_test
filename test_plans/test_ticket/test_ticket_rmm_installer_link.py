import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
from uuid import uuid4
import variables
from time import sleep
from playwright.sync_api import expect


@pytest.mark.regression
def test_customer_assets_new_rmm_installer(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'IService' + str(uuid4()))
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child > a[class="btn btn-default btn-sm dropdown-toggle"]')
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child a:has-text("RMM Agent Installer")')

    page.wait_for_timeout(1000)
    assert page.wait_for_selector('text=Create an RMM Agent')

    # Verify that RMM Installer url exist in the GET RMM AGENT INSTALLER form
    assert 'https://rmm.syncrostaging1.com/dl/rs/' in page.locator('div.well.mtm.text-wrap').inner_text()

    page.click('input[value="cmd"]')
    sleep(0.1)
    # expect(page.locator('div[class="well mtm text-wrap"]')).to_contain_text(f"--customerid {customer.customer_id}")
    expect(page.locator('div[id="_customer_id"]')).to_contain_text(customer.business_name)
    expect(page.locator('span[id="_policy_folder_id"]')).to_contain_text(customer.business_name)
