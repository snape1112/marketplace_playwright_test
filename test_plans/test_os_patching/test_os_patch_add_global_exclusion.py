import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from playwright.sync_api import Page
import variables

def disabled_test_os_patch_add_global_exclusion (page: Page, login):
    # customer_name = str(uuid.uuid4())
    # create_customer(customer_name, api_request_context)

    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] >> text=Admin')
    page.click('text=Windows Patching')
    assert page.wait_for_selector('text="Global Patch Exclusion List"') != None
    assert page.wait_for_selector('text="There are no globally excluded patches."') != None   
    page.click('text=Add A Global Patch Exclusion')
    dialog_text = page.wait_for_selector('text=Add Global Patch Exclusion')
    assert dialog_text != None
    page.fill('[placeholder="########"]','12345')
    ##description  = page.wait_for_selector("//*[@class ='form-control string optional]")
    page.fill("//*[@class ='form-control string optional']", 'some description')
    page.click('button:has-text(\"Save\")')
    success_message = page.wait_for_selector('text=Successfully created 1 exclusion')
    assert success_message != None
    new_patch = page.wait_for_selector('text=KB12345')
    assert new_patch !=None
    patch_list_description = page.wait_for_selector ('text=List of patches that are to be excluded from managed services.')
    assert patch_list_description !=None
    page.click('text=Remove')
    assert page.wait_for_selector('text=Patch exclusion successfully removed.') != None
    




 
