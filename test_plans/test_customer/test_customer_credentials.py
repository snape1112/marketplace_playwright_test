import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
import uuid
from playwright.sync_api import expect
import variables

@pytest.mark.regression
def test_customer_credentials(page, login, api_request_context):

    # Preconditions: create customers
    customer = Customer(business_name = 'IService' + str(uuid.uuid4()))
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')

    page.click('ul.nav.nav-tabs a:has-text("Credentials")')

    # Make new Credential
    page.click('div.customer-credentials-root a:has-text("New Credential")')

    page.wait_for_timeout(5000) # Wait for best in place inputs to load

    # Verify New Credential fields
    expect(page.locator('span[data-bip-attribute="name"]')).to_contain_text('New Credential')

    expect(page.locator('span[data-bip-attribute="username"]')).to_contain_text('-')

    expect(page.locator('span[data-bip-attribute="host_url"]')).to_contain_text('-')

    expect(page.locator('table.table-striped tbody td >> nth=3')).to_contain_text('*****')

    expect(page.locator('table.table-striped tbody td >> nth=4')).to_contain_text('-')

    expect(page.locator('span[data-bip-type="checkbox"]')).to_contain_text('Private')

    # Fill in Name
    page.click('span[data-bip-attribute="name"]')
    page.fill('form.form_in_place input[name="name"]', 'New test credential')

    # Fill in Username
    page.click('span[data-bip-attribute="username"]')
    page.fill('form.form_in_place input[name="username"]', 'Ben Beck')

    # Fill in HOST/URL
    page.click('span[data-bip-attribute="host_url"]')
    page.fill('form.form_in_place input[name="host_url"]', 'https://test.syncromsp.com')

    # Fill in Password
    page.click('span.hidden-credential')
    page.wait_for_timeout(5000) # Wait for best in place to appear instead of *****
    page.click('span[data-bip-attribute="password"]')
    page.fill('form.form_in_place input[name="password"]', 'password1')

    # Fill in Notes
    page.click('table.table-striped tbody td >> nth=4')
    page.fill('form.form_in_place textarea[name="notes"]', 'My test credential notes')
    page.click('form.form_in_place input[value="Save"]')

    # Click on Public/Private
    page.click('span[data-bip-type="checkbox"]')

    # Verify Credential fields

    expect(page.locator('span[data-bip-attribute="name"]')).to_contain_text('New test credential')

    expect(page.locator('span[data-bip-attribute="username"]')).to_contain_text('Ben Beck')

    expect(page.locator('span[data-bip-attribute="host_url"]')).to_contain_text('https://test.syncromsp.com')

    expect(page.locator('table.table-striped tbody td >> nth=3')).to_contain_text('password1')

    expect(page.locator('table.table-striped tbody td >> nth=4')).to_contain_text('My test credential notes')

    expect(page.locator('span[data-bip-type="checkbox"]')).to_contain_text('Public on Customer Portal')

