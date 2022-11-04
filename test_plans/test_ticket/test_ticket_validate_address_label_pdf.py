from time import sleep
import time
import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import variables

def test_ticket_validate_address_label_pdf(page, login, api_request_context):
    customer_name = str(uuid.uuid4())
    customer_id, _ = create_customer(customer_name, api_request_context)
    quick_view_selector = '#quick-view-customer-{}'.format(customer_id)
    create_ticket(customer_id, api_request_context)
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)
    page.click('a[class="btn btn-default dropdown-toggle  tooltipper"] > i[class="fas fa-caret-down"]')
    with page.context.expect_page() as new_page_info:
        page.click('text=Address Label')
    tab=new_page_info.value
    print(tab.url)

   #verifies lines
    page.wait_for_timeout(2000)
    line1 = tab.locator('#labels_line1').get_attribute('value')
    assert line1==customer_name
    line2 = tab.locator('#labels_line2').get_attribute('value')
    assert line2=='string'
    line3 = tab.locator('#labels_line3').get_attribute('value')
    assert line3=='string'
    line4 = tab.locator('#labels_line4').get_attribute('value')
    assert line4=='string, string string'

    width = tab.locator('#labels_width').get_attribute('value')
    assert width=='300'

    height = tab.locator('#labels_height').get_attribute('value')
    assert height=='100'
