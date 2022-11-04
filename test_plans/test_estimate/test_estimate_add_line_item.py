import pytest
import re
import uuid 
from fixtures.login import create_account, login
from helpers.estimate import create_estimate, create_estimate_with_line_item
from helpers.customer import create_customer
import variables

@pytest.mark.regression
def test_estimate_add_line_item(page, login, api_request_context):
        customer_name = str(uuid.uuid4())
        create_customer(customer_name, api_request_context)
        create_estimate(page, customer_name)

        page.type('#line_item_item','Labor', delay=150)
        page.click("text='Labor - Labor'")   
        page.click('text=Create Line item')
        page.click('span:has-text("120.00")')
        page.fill('input[name="price"]', '300')
        with page.expect_navigation():
                page.click('input:has-text("Save")')
        message = page.wait_for_selector('#line_items_table >> text=300.00')
        assert message != None

@pytest.mark.regression
def test_convert_estimate_to_invoice(page, login, api_request_context):
        customer_name = str(uuid.uuid4())
        create_customer(customer_name, api_request_context)
        create_estimate_with_line_item(page, customer_name)
        
        # This find the "Estimate #" text in the upper left of the Estimate page and parses out the number portion.
        estimate_value = page.locator('text=/Estimate #(\d+)/').inner_text()
        estimate_number_result = re.search(r"(\d+)", estimate_value)
        estimate_number = estimate_number_result.group(0)
        
        # This will get the Estimate ID from the URL.  This is the db row number of the record.
        estimate_full_url = page.url
        parsed_estimate_id = re.search(r'(?<=estimates\/)(\d+)', estimate_full_url)
        estimate_id = parsed_estimate_id.group(0)

        # Make the Invoice
        page.click('text=Convert to Invoice')
        message = page.wait_for_selector('text=Converted')
        assert message != None
        
        # Clicks the Estimate number to return to the Estimate
        page.locator(f'a:has-text("{estimate_number}")').click()

        # Verify we are back on the estimate
        estimate_return_url = page.url
        parsed_return = re.search(r'(?<=estimates\/)(\d+)', estimate_return_url)
        estimate_return_id = parsed_return.group(0)
        assert estimate_id == estimate_return_id

        # Verify the Estimate is now "Approved" since it was converted
        estimate_approved = page.wait_for_selector('text=Approved')
        assert estimate_approved != None