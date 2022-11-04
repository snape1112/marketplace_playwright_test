import pytest
from fixtures.constants import *
from playwright.sync_api import Page
import re
import variables

def create_new_invoice(page : Page, customer_name : str) -> str:
    """
            Creates a new invoice and a line item
            Arguments:
            page: a Page
            customer_name: a string
            Returns:
            Creates the new estimate with a line item for the customer and returns the database id
    """        
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/invoices')

    page.click('#new_search >> text=New Invoice')
    page.click('#invoice_customer_name')
    page.type('#invoice_customer_name',customer_name[:5], delay=150)
    page.click(f'text=/{customer_name[:5]}.*/')
    page.click('text=Create Invoice')   
    page.wait_for_selector('text=Created successfully') != None
    assert page.wait_for_selector('text=Created successfully')
    parsed_invoice_id = re.search(r'(?<=invoices\/)(\d+)', page.url)
    return parsed_invoice_id.group(0)

def create_invoice_with_line_item(page : Page, customer_name : str) -> str:
    """
            Creates a new invoice and a line item
            Arguments:
            page: a Page
            customer_name: a string
            Returns:
            Creates the new invoice with a line item for the customer and returns the database id
    """
    invoice_id = create_new_invoice(page, customer_name) 
    page.type('#line_item_item','Labor', delay = 150)    
    page.click('text="Labor - Labor"')   
    page.click('text=Create Line item')
    page.click('[data-bip-attribute=price]')
    page.fill('input[name="price"]', '300')
    with page.expect_navigation():
            page.click('input:has-text("Save")')
    return invoice_id

def invoice_add_line_item(page : Page) -> str:
    """
            Creates a new invoice and a line item
            Arguments:
            page: a Page
            customer_name: a string
            Returns:
            Creates the new invoice with a line item for the customer and returns the database id
    """
    page.type('#line_item_item','Labor', delay = 150)
    page.click('text="Labor - Labor"')
    page.click('text=Create Line item')
    page.click('[data-bip-attribute=price]')
    page.fill('input[name="price"]', '300')
    with page.expect_navigation():
            page.click('input:has-text("Save")')