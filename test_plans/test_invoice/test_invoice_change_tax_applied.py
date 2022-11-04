# https://repairtechsolutions.atlassian.net/browse/QA-1402
from time import sleep
import pytest
import uuid
from fixtures.constants import *
from playwright.sync_api import Page
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import re
import variables


@pytest.mark.regression
def test_invoice_change_tax_applied(page: Page, login, api_request_context):

    # Pre-condition

    customer_name = str(uuid.uuid4()) 
    create_customer(customer_name, api_request_context) 
    create_new_invoice(page, customer_name)

    # Create line item

    page.click('a:has-text("Add Manual Item")')
    page.wait_for_load_state('domcontentloaded')
    page.select_option('#category_ids', label='Default')
    page.fill('[placeholder="A Short Description"]', 'test')
    page.fill('#line_item_price',  '20.00')
    page.fill('#line_item_cost',  '20.00')
    page.click('//*[@id="new_line_form_manual"]/div[4]/div[11]/input')
    label = page.wait_for_selector('text="Added a line item successfully."')
    assert label != None

    # Change Product Category - Not working
    manual_line_item_url_regex_result = re.search(
        r"(/invoices/\d+/line_items/\d+)", page.content())
    line_item_url = manual_line_item_url_regex_result.group(0)

    manual_line_item_id_regex_result = re.search(
        r"/invoices/\d+/line_items/(\d+)",  line_item_url)
    line_item_id = manual_line_item_id_regex_result.group(1)
    auth_locator = page.locator('meta[name="csrf-token"]')
    token = auth_locator.get_attribute('content')
    assert token != None
    r = 'var formData = new FormData();'
    r += 'formData.append("_method", "put");'
    r += 'formData.append("line_item[taxable]", "false");'
    r += f'formData.append("authenticity_token", "{token}");'
    r += 'var xhr = new XMLHttpRequest();'
    r += f'xhr.open("PUT", "https://{variables.subdomain}.{BASE_DOMAIN}{line_item_url}", true);'
    r += 'xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");'
    r += 'xhr.send(new URLSearchParams(formData));'
    x = page.evaluate(r,)
    page.reload()
    page.evaluate(
        f'$(".advanced-line-{line_item_id}").toggleClass("visibility-collapse")')


    # Validate tax is changed

    assert page.locator(f'#best_in_place_line_item_{line_item_id}_taxable').first.inner_text() == 'No'  
   