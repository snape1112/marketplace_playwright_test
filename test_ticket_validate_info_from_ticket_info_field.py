import datetime
from datetime import timedelta
import enum
import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import variables


def test_ticket_validate_ticket_info_fields(page, login, api_request_context):
    customer_name = str(uuid.uuid4())
    customer_id = create_customer(customer_name, api_request_context)
    new_due_date = datetime.datetime.now() + timedelta(days=3, hours=-3)
    ticket_id, ticket_num = create_ticket(customer_id,api_request_context)
    quick_view_selector = '#quick-view-ticket-{}'.format(ticket_id)

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    page.wait_for_timeout(100)
    page.wait_for_selector(quick_view_selector)
    page.click(quick_view_selector) 


    expect(page.locator(f"[class=qv-title] a")).to_have_text(f"#{ticket_num}")
    expect(page.locator(f"[class=qv-subtitle]")).to_have_text("Printer not working")

    ticket_details = [
        ["Customer", customer_name],
        ["Assignee", ""],
        ["Issue", "Remote Support"],
        ["Last Updated", "less than a minute"],
        ["Due Date", new_due_date.strftime("%d %b %H:%M")]
    ]

    for index, row in enumerate(ticket_details):
        tr = "tr:first-child" if not index else f"tr:nth-child({index + 1})"
        expect(page.locator(f"div[class='qv-details'] td[class='qv-details-left'] table {tr} th")).to_have_text(row[0])
        expect(page.locator(f"div[class='qv-details'] td[class='qv-details-left'] table {tr} td")).to_have_text(row[1])
