import pytest
import uuid 
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
import variables


@pytest.mark.regression
def test_invoice_add_product(page, login, api_request_context):
 
    # Pre-condition

    customer_name = str(uuid.uuid4()) 
    create_customer(customer_name, api_request_context) 

    product_serial = str(uuid.uuid4())
    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] >> text=Products & Services')
    page.click('text=New Item')

    # Create a new product with a serial number

    page.fill('#product_name','Test product for invoice')
    page.fill('textarea[name="product[description]"]','Test product for invoice')
    page.check('text=Serialized >> input[name="product[serialized]"]')
    page.click('text=Add serial numbers') 
    page.click('#product_tags_product_serials_addTag') 
    page.fill('#product_tags_product_serials_tag', product_serial)
    page.click('text=Close') 
    page.fill('#product_upc_code', str(uuid.uuid4())) 
    page.fill('#product_price_retail','10')
    page.fill('#product_price_cost','10')
    page.select_option('#category_ids', label='Default')
    page.fill('#product_sort_order','0')
    page.click('#product-details >> text=Create Product') 
    message = page.wait_for_selector('text="Product was successfully created."')
    assert message != None

    # Create a new invoice

    create_new_invoice(page, customer_name)
    page.type('#line_item_item','Test product for', delay=150)
    page.click(f'text=/Test product for.*/')
    page.click('text=Create Line item')
    page.click('text=Select serials')  

    # Select the serial number that we created above

    page.check(f'//*[@id="spsw-serials_"]')
    with page.expect_navigation():
        page.click("text=Save Changes")

    # Assert that the subtotal matches the price that we seet above
    assert page.wait_for_selector('#line_items_table >> text=Subtotal $10.00') != None
    assert page.wait_for_selector(f'text={product_serial}') != None
 