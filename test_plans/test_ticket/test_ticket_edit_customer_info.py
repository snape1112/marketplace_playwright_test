from time import sleep
import time
from xml.sax.xmlreader import Locator
import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.ticket import create_ticket
from playwright.sync_api import expect
import variables



def test_ticket_edit_customer_info(page, login, api_request_context):
    customer_name = str(uuid.uuid4())
    customer_id, _  = create_customer(customer_name, api_request_context)
    quick_view_selector = '#quick-view-customer-{}'.format(customer_id)
    create_ticket(customer_id, api_request_context)
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)
    page.click('text="Edit"')

    #Editing
    page.fill('#customer_firstname', 'first' + customer_name)
    page.fill('#customer_lastname', 'last' + customer_name)
    page.fill('#customer_business_name', 'edited' + customer_name)
    page.fill('#customer_email', 'email' + customer_name + '@syncromsp.com')
    page.fill('#customer_phones_attributes_0_number', '122-345-6789')
    page.fill('#customer_address_2', 'address' + customer_name)
    page.fill('#customer_city', 'city' + customer_name)
    page.fill('#customer_state', 'state' + 'CA')
    page.fill('#customer_zip', 'zip' + '92111')
    page.click('text="Save Changes"')

    assert page.wait_for_selector('text=/Customer successfully.*/') != None

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)


    expect(page.locator('//*[@class="qv-title"]/a')).to_contain_text('first'+customer_name)
    expect(page.locator('//*[@class="qv-title"]/a')).to_contain_text('last'+customer_name)
    expect(page.locator('//*[@class="qv-title"]/a')).to_contain_text('edited'+customer_name)
    expect(page.locator('//*[@class="qv-details-title"]/following-sibling::table/tbody/tr[1]/td/a')).to_contain_text('email' + customer_name + '@syncromsp.com')
    expect(page.locator('//*[@class="qv-details-title"]/following-sibling::table/tbody/tr[2]/td/a[1]').first).to_contain_text('122-345-6789')
    expect(page.locator('//*[@class="qv-details-title"]/following-sibling::table/tbody/tr[3]/td/a')).to_contain_text('address' + customer_name)
    expect(page.locator('//*[@class="qv-details-title"]/following-sibling::table/tbody/tr[3]/td/a')).to_contain_text('city' + customer_name)
    expect(page.locator('//*[@class="qv-details-title"]/following-sibling::table/tbody/tr[3]/td/a')).to_contain_text('state' + 'CA')
    expect(page.locator('//*[@class="qv-details-title"]/following-sibling::table/tbody/tr[3]/td/a')).to_contain_text('zip' + '92111')
