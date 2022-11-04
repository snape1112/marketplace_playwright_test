import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from playwright.sync_api import Page
import re
import variables

def create_estimate(page : Page, customer_name : str) -> str: 
    """
            Creates a new estimate
            Arguments:
            page: a Page
            customer_name: a string
            Returns:
            Creates the new estimate with the customer and returns the database id
    """
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/estimates')
    page.locator('a:has-text("New Estimate")').nth(1).click()
    page.click('#estimate_customer_name')
    page.type('#estimate_customer_name',customer_name[:5], delay=150)
    page.click(f'text=/{customer_name[:5]}.*/')
    page.click('text=Create estimate')     
    assert page.wait_for_selector('text=Created successfully')
    parsed_estimate_id = re.search(r'(?<=estimates\/)(\d+)', page.url)
    return parsed_estimate_id.group(0)       



def create_estimate_with_line_item(page : Page, customer_name : str) -> str: 

    """
            Creates a new estimate and a line item
            Arguments:
            page: a Page
            customer_name: a string
            Returns:
            Creates the new estimate with a line item for the customer and returns the database id
    """
    estimate_id = create_estimate(page, customer_name)
    page.type('#line_item_item','Labor', delay=150)
    page.click('text=Labor - Labor')   
    page.click('text=Create Line item')
    assert page.wait_for_selector('text=Added a line item successfully.') != None
    return estimate_id