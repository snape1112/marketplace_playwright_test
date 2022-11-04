import datetime
from datetime import timedelta
import enum
from time import sleep
import time
import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.customer import Customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import variables


def test_customer_new_reminder(page, login, api_request_context):
    customer = Customer(business_name = 'John' + str(uuid.uuid4())[1:10], first_name = 'John', last_name = 'Smith')
    customer.create(api_request_context)

    page.goto(f'{variables.base_url}/customers/{customer.customer_id}')
    page.wait_for_timeout(100)
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child > a[class="btn btn-default btn-sm dropdown-toggle"]')
    page.click('div[class="col-md-6 btn-bar title-btns by-right"] > div:first-child a[href="#new-reminder"]')

    time.sleep(1)

    reminder_date = datetime.datetime.now() + timedelta(days=10)
    round_time = lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 15*(dt.minute // 15))
    reminder_date = round_time(reminder_date)
    page.evaluate(f'$("#reminder_modal_reminder_at_time_label").datepicker( "setDate", "{reminder_date}" )',)
    reminder_note = "It's time to have a meeting."
    page.fill("#reminder_modal_reminder_message", reminder_note)
    page.click("input[value='Save Reminder'][class='btn btn-sm btn btn-success btn-teal btn-sm right']")

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/reminders')
    #page.wait_for_timeout(100)

    reminder_fields = [reminder_note, reminder_date.strftime("%a %m-%d-%y %I:%M %p"), variables.admin_name, customer.business_name]

    for index, value in enumerate(reminder_fields):
        if index == 0:
            td = "th"
        else:
            td = f"td:nth-child({index + 1})"
        expect(page.locator(f"table[class='table-striped borderless tablesaw tablesaw-stack table-condensed remindersTable sticky'] tbody tr:first-child {td}")).to_have_text(value)
