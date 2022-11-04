import pytest
import uuid
import re
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import variables

@pytest.mark.regression
def test_exercise_line_item_fields(page, login, api_request_context):

        
        # Pre-condition

        customer_name = str(uuid.uuid4()) 
        create_customer(customer_name, api_request_context)
        create_new_invoice(page, customer_name)

        # Add new line item
        page.type('#line_item_item','Labor', delay=150)
        page.click('text="Labor - Labor"')   
        page.click('text=Create Line item')
        
        # This will capture the line item number. Now I can reference it in any calls to items in the overflow
        line_item_number = page.locator('tr[id^=line_item_]')
        line_item_number_regex_result = re.search(r"(\d+)", line_item_number.get_attribute('id'))
        line_item_number = line_item_number_regex_result.group(0)

        # Change Description
        page.click(f'#best_in_place_line_item_{line_item_number}_name')
        page.fill('textarea[name="name"]', "Changed Desc")
        page.click('text=SaveCancel >> input[type="submit"]')
        description = page.locator(f'#best_in_place_line_item_{line_item_number}_name').first.inner_text()
        assert description == 'Changed Desc'  

        # Quantity
        page.click('[data-bip-attribute=quantity]')
        page.fill('input[name="quantity"]', "2")
        with page.expect_navigation():
                page.click('input:has-text("Save")', delay=500)
        qty = page.locator(f'#best_in_place_line_item_{line_item_number}_quantity').first.inner_text()
        assert qty == '2.0' 

        # Change the Rate/Price
        page.click('[data-bip-attribute=price]')
        page.fill('input[name="price"]', "300")
        with page.expect_navigation():
                page.click('input:has-text("Save")', delay=500)
        price_all = page.locator(f'#best_in_place_line_item_{line_item_number}_price').first.inner_text()
        price_reg = re.search(r"((\d+)\.(\d+))", price_all)
        price = price_reg.group(0)
        assert price == '300.00' 

        #Taxable/Tax - Works!
        line_item_url_regex_result = re.search(r"(/invoices/\d+/line_items/\d+)", page.content())
        line_item_url = line_item_url_regex_result.group(0)
        auth_locator = page.locator('meta[name="csrf-token"]')
        token = auth_locator.get_attribute('content')
        assert token != None
        taxable = 'var formData = new FormData();'
        taxable += 'formData.append("_method", "put");'
        taxable += 'formData.append("line_item[taxable]", "false");'
        taxable += f'formData.append("authenticity_token", "{token}");'
        taxable += 'var xhr = new XMLHttpRequest();'
        taxable += f'xhr.open("PUT", "https://{variables.subdomain}.{BASE_DOMAIN}{line_item_url}", true);'
        taxable += 'xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");'
        taxable += 'xhr.send(new URLSearchParams(formData));'
        taxable_x = page.evaluate(taxable,)
        page.reload()
        taxable = page.locator(f'#best_in_place_line_item_{line_item_number}_taxable').first.inner_text()
        # UI Yes = DB true
        # UI No  = DB false
        assert taxable == 'No' 

        # Expands the line item row overflow
        page.click('a[class="btn btn-default btn-sm"]')

        #  Change Product Category
        line_item_url_regex_result = re.search(
            r"(/invoices/\d+/line_items/\d+)", page.content())
        line_item_url = line_item_url_regex_result.group(0)
        # Gets the Auth Token from headers
        auth_locator = page.locator('meta[name="csrf-token"]')
        token = auth_locator.get_attribute('content')
        assert token != None
        # Create a POST 'message' to change the value in the DB directly
        prod_cat = 'var formData = new FormData();'
        prod_cat += 'formData.append("_method", "put");'
        prod_cat += 'formData.append("line_item[product_category]", "Hardware");'
        prod_cat += f'formData.append("authenticity_token", "{token}");'
        prod_cat += 'var xhr = new XMLHttpRequest();'
        prod_cat += f'xhr.open("PUT", "https://{variables.subdomain}.{BASE_DOMAIN}{line_item_url}", true);'
        prod_cat += 'xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");'
        prod_cat += 'xhr.send(new URLSearchParams(formData));'
        prod_cat_x = page.evaluate(prod_cat,)
        # Reloads the page to get the updated DB value
        page.reload()
        # Expand overflow
        page.click('a[class="btn btn-default btn-sm"]')
        product_category = page.locator(f'#best_in_place_line_item_{line_item_number}_product_category').first.inner_text()
        assert product_category == 'Hardware' 


        # Tax Note
        page.click(f'#best_in_place_line_item_{line_item_number}_tax_note')
        page.fill('input[name="tax_note"]', "Free Tax")
        page.click('text=SaveCancel >> input[type="submit"]')
        tax_note = page.locator(f'#best_in_place_line_item_{line_item_number}_tax_note').first.inner_text()
        assert tax_note == 'Free Tax' 

        # Discount - Cannot have discount % and Discount $ at the same time.
        page.click('[data-bip-attribute=discount_dollars]')
        page.fill('input[name="discount_dollars"]', "13")
        with page.expect_navigation():
                page.click('input:has-text("Save")', delay=500)
        # Expands the line item row overflow
        page.click('a[class="btn btn-default btn-sm"]')
        # Formats the output - puts it in nn.nn format and removes any currency symbols
        discount_dollars_all = page.locator(f'#best_in_place_line_item_{line_item_number}_discount_dollars').first.inner_text()
        discount_dollars_reg = re.search(r"((\d+)\.(\d+))", discount_dollars_all)
        discount_dollars = discount_dollars_reg.group(0)
        assert discount_dollars == '13.0' 


        # Cost
        page.click('[data-bip-attribute=cost]')
        page.fill('input[name="cost"]', "23")
        with page.expect_navigation():
                page.click('input:has-text("Save")', delay=500)
        # Expands the line item row overflow
        page.click('a[class="btn btn-default btn-sm"]')
        # Formats the output - puts it in nn.nn format and removes any currency symbols
        cost_all = page.locator(f'#best_in_place_line_item_{line_item_number}_cost').first.inner_text()
        cost_reg = re.search(r"((\d+)\.(\d+))", cost_all)
        cost = cost_reg.group(0)
        assert cost == '23.00' 