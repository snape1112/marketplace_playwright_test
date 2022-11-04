import pytest
import uuid
from fixtures.login import create_account, login
from helpers.customer import create_customer
from helpers.invoice import create_new_invoice
from playwright.sync_api import Page
import re
import variables

@pytest.mark.regression
def test_invoice_add_product_bundle(page, login, api_request_context):

    # Pre-condition
    customer_name = str(uuid.uuid4())
    create_customer(customer_name, api_request_context)
    create_new_invoice(page, customer_name)

    product_serial = str(uuid.uuid4())
    product_id = str(uuid.uuid4())
    bundle_name = str(uuid.uuid4())
    upc_code = str(uuid.uuid4())

    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] >> text=Products & Services')
    page.click('text=New Item')

    # Create a new product with a serial number
    page.fill('#product_name', product_id)
    page.fill('textarea[name="product[description]"]', product_id)
    page.check('text=Serialized >> input[name="product[serialized]"]')
    page.click('text=Add serial numbers')
    page.click('#product_tags_product_serials_addTag')
    page.fill('#product_tags_product_serials_tag', product_serial)
    page.click('text=Close')
    page.fill('#product_upc_code', upc_code)
    page.fill('#product_price_retail','10')
    page.fill('#product_price_cost','10')
    page.select_option('#category_ids', label='Default')
    page.fill('#product_sort_order','0')
    page.click('#product-details >> text=Create Product')
    success_label = page.locator(f'text="Product was successfully created."').first.inner_text()
    assert success_label.endswith('Product was successfully created.')

    # Create new bundle

    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] >> text=Products & Services')
    page.click('text="Inventory Modules"')
    page.click('text=Bundle Items')
    page.click('text=New Inventory Bundle')
    page.fill('input[name="inventory_bundle[name]"]',f'{bundle_name}')
    page.fill('textarea[name="inventory_bundle[description]"]',f'{bundle_name}')
    page.fill('input[name="inventory_bundle[upc_code]"]',f'{upc_code}')
    page.click('text=Create Inventory bundle')

    # Update retail price

    parsed_return = re.search(r'/inventory_bundles/(\d+)', page.url)
    bundle_id = parsed_return.group(1)

    page.click(f'#best_in_place_inventory_bundle_{bundle_id}_price_retail')
    page.fill('input[name=\"price_retail\"]','100')
    with page.expect_navigation():
        page.click('text=SaveCancel >> input[type=\"submit\"]')

    # Validate fields

    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] >> text=Products & Services')
    page.click('text="Inventory Modules"')
    page.click('text=Bundle Items')
    page.click(f'text={bundle_name}')

    bundle_name_label = page.locator(f'#best_in_place_inventory_bundle_{bundle_id}_name').first.inner_text()
    assert bundle_name == bundle_name_label

    upc_code_label = page.locator(f'#best_in_place_inventory_bundle_{bundle_id}_upc_code').first.inner_text()
    assert upc_code == upc_code_label

    retail_price_label = page.locator(f'#best_in_place_inventory_bundle_{bundle_id}_price_retail').first.inner_text()
    assert '$100.00' == retail_price_label

    short_product = product_id[0:5]
    page.type('#bundle_item',short_product, delay=150)
    page.click(f'text=/{short_product}.*/')

    page.fill('#bundle_quantity', '100')
    page.click('[name=commit]')
    quantity = page.locator(f'text=100.0').first.inner_text()
    assert '100.0' == quantity
