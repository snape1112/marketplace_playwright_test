import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
import uuid
from playwright.sync_api import expect
import variables
import re

@pytest.mark.regression
def test_customer_comunications(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'IService' + str(uuid.uuid4()), first_name = 'John', last_name = 'Smith')
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')
    # Click Communications
    page.click('ul.nav.nav-tabs a:has-text("Communications")')

    # Create 4 Comunications with different types
    page.type('form#new_communication_log textarea#communication_log_big_note', 'Test communications 1')
    page.click('input[value=Submit]')
    page.wait_for_timeout(5000)

    page.type('form#new_communication_log textarea#communication_log_big_note', 'Test communications 2')
    page.select_option('select#communication_log_communication_type', 'Email')
    page.click('input[value=Submit]')
    page.wait_for_timeout(5000)

    page.type('form#new_communication_log textarea#communication_log_big_note', 'Test communications 3')
    page.select_option('select#communication_log_communication_type', 'Visit')
    page.click('input[value=Submit]')
    page.wait_for_timeout(5000)

    page.type('form#new_communication_log textarea#communication_log_big_note', 'Test communications 4')
    page.select_option('select#communication_log_communication_type', 'Other')
    page.click('input[value=Submit]')

    # Verify Cummunications fields
    # Phone
    expect(page.locator('div.communication_log_entry:has-text("Test communications 1")')).to_contain_text('Phone')
    date = page.locator('div.communication_log_entry:has-text("Test communications 1") div.col-xs-5 span.meta').inner_text()
    # Verify date
    assert re.match(r'(MON|TUE|WED|THU|FRI|SAT|SUN) \d{1,2}:\d\d\w\w', date)

    # Email
    expect(page.locator('div.communication_log_entry:has-text("Test communications 2")')).to_contain_text('Email')
    # Verify date
    date = page.locator('div.communication_log_entry:has-text("Test communications 2") div.col-xs-5 span.meta').inner_text()
    assert re.match(r'(MON|TUE|WED|THU|FRI|SAT|SUN) \d{1,2}:\d\d\w\w', date)

    # Visit
    expect(page.locator('div.communication_log_entry:has-text("Test communications 3")')).to_contain_text('Visit')
    date = page.locator('div.communication_log_entry:has-text("Test communications 3") div.col-xs-5 span.meta').inner_text()
    assert re.match(r'(MON|TUE|WED|THU|FRI|SAT|SUN) \d{1,2}:\d\d\w\w', date)

    # Other
    expect(page.locator('div.communication_log_entry:has-text("Test communications 4")')).to_contain_text('Other')

    # Verify date
    date = page.locator('div.communication_log_entry:has-text("Test communications 4") div.col-xs-5 span.meta').inner_text()
    assert re.match(r'(MON|TUE|WED|THU|FRI|SAT|SUN) \d{1,2}:\d\d\w\w', date)

    # Delete Communication with type is Phone
    page.click('div.communication_log_entry:has-text("Test communications 1") a:has-text("•••")')

    page.on("dialog", lambda dialog: dialog.accept())
    # Click 'Delete'
    page.click('div.communication_log_entry:has-text("Test communications 1") button:has-text("Delete")')

    # Veify that Communication with type Phone was deleted

    expect(page.locator('div#communicationLogs')).not_to_contain_text("Test communications 1")
    expect(page.locator('div#communicationLogs')).not_to_contain_text("Phone")

