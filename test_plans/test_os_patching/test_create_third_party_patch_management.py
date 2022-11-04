#https://repairtechsolutions.atlassian.net/browse/QA-1231
import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login 
from playwright.sync_api import Page
import variables

def disable_test_create_third_party_patch_management_policy (page: Page, login):
    policy_name = str(uuid.uuid4())
    page.click('a[role="button"]:has-text("More")')
    page.click('ul[role="menu"] >> text=Policies')
   

    page.click('text=Policy Modules')
    page.click('text=Third Party Patch Management') 
    page.click('text=New Third Party Patch Management Policy')
    page.fill('id=application_management_policy_name',policy_name)
    page.click('text=If offline, run at next boot')
    page.check('.application_management_policy_next_boot >> text=If offline, run at next boot')
    page.fill('id=application_management_policy_boot_delay', '020')
    page.click('input:has-text("Save")')
    policy = page.wait_for_selector(f'text="{policy_name}"')
    assert policy != None
