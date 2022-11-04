import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
import uuid
from playwright.sync_api import expect
import variables
import re

@pytest.mark.regression
def test_customer_reminder(page, login, api_request_context):

    # Preconditions: create customer
    customer = Customer(business_name = 'IService' + str(uuid.uuid4()), first_name = 'John', last_name = 'Smith')
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')

    # Create new reminder
    page.click('div.widget.borderless.overflowable:has-text("Reminders") a:has-text("New")')

    page.fill('textarea#reminder_modal_reminder_message', 'Test Reminder Notes')
    page.click('input#reminder_modal_reminder_at_time_label')

    # Click on the 'Next' month button in the datepicker
    page.click('a.ui-datepicker-next:has-text("Next")')
    page.wait_for_timeout(1000)

    # Choose '14'th day from the datepicker
    page.click('a.ui-state-default:has-text("14")')
    page.wait_for_timeout(1000)
    page.click('button.ui-datepicker-close:has-text("Done")')
    page.wait_for_timeout(2000)

    page.click('input:has-text("Save Reminder")')

    # Verify that reminder with note 'Test Reminder Notes' exist on the page customer show
    expect(page.locator('div.widget-content.reminders-table')).to_contain_text('Test Reminder Notes')

    date = page.locator('div.widget-content.reminders-table').inner_text()
    # Verify that reminder date contains month and date that we set
    assert re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) 14', date)
