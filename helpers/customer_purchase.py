import pytest
from fixtures.constants import *
from playwright.sync_api import Page
import re
import variables

def create_customer_purchase(page : Page, customer_business_name : str, enable_setting=True ) -> str:
    """
            Creates a new purcase
            Arguments:
            page: a Page
            customer_name: a string
            Returns:
            Creates the new purcase for the customer and returns the database id
    """

    # Head to Admin > Inventory - Preferences to enable purchasing
    if enable_setting :
        page.click('span:has-text("More")')
        page.click('ul[role="menu"] a:has-text("Admin")')
        page.click('ul#inventoryCollapse li:has-text("Preferences")')
        page.check('input#settings_enable_purchasing')
        page.click('input.btn-success:has-text("Save")')

    page.goto(f'{variables.base_url}/customer_purchases')
    # Click New Customer Purchase
    page.click('div.row.pbm a.btn.btn-teal:has-text("New Customer Purchase")')

    page.type('input#customer_purchase_customer_name', customer_business_name[:10], delay = 150)
    page.click(f'text=/{customer_business_name[:10]}.*/')
    page.wait_for_timeout(1000)
    page.click('text="Create Customer purchase"')

    assert page.wait_for_selector('text="Customer purchase was successfully created."')

    parsed_purchase_id = re.search(r'(?<=purchases\/)(\d+)', page.url)
    return parsed_purchase_id.group(0)

def set_customer_purchase_status(page : Page, status: str):
    page.click('span[data-bip-attribute="status"]')
    page.wait_for_timeout(1000) # let best in place open
    page.click('span[data-bip-attribute="status"]')
    page.select_option('span[data-bip-attribute="status"] select', status)
    page.wait_for_timeout(5000) # let best in place send data to the server

# Add Item to the Purchase (Manual New Inventory Item)
def add_manual_item_to_customer_purchase(page : Page):
    page.fill('div.widget-content:has-text("Manual New") input#customer_purchase_line_item_name', 'Acer')
    page.fill('textarea#customer_purchase_line_item_description', 'Laptop')

    page.fill('div.widget-content:has-text("Manual New") input#customer_purchase_line_item_price_cost', '200')
    page.wait_for_timeout(5000)
    page.click('div.widget-content:has-text("Manual New") input:has-text("Add Item")')

    assert page.wait_for_selector('text="Added the item"')

    # Pay for Customer Purchase
    page.click('a:has-text("Pay Out")')

    page.select_option('select#customer_purchase_payment_method_id', label='Cash')
    page.wait_for_timeout(2000) # wait to ensure Flash will work on the next page
    page.click('input[value="Record Payment"]')

    assert page.wait_for_selector('text="Alright! Marked as paid and accepted"')

