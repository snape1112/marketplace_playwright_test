import pytest
import uuid
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.user import create_tech_and_login
from playwright.sync_api import expect
import variables

# Create Public Ticket Search or Private Ticket Search
def create_ticket_search(page, public = True):
    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')
    if public:
        public_or_private = 'Public'
    else:
        public_or_private = 'Private'
    # Create Public or Private Ticket Search
    page.click('a.btn.btn-default.btn-sm.dropdown-toggle')
    page.click('text=Create New')

    # Set New Saved Ticket Search name
    page.fill('input#ticket_search_name', f'{public_or_private} Filter')

    # Set ticket search as not default
    page.select_option('select#ticket_search_set_as_default', value = 'false')

    # Set ticket search as Puplic or Private
    page.select_option(f'select#ticket_search_public', label = public_or_private)

    # Click 'Create Ticket Search' button
    page.click('input:has-text("Create Ticket Search")')

@pytest.mark.regression
def test_ticket_search(page, login, api_request_context):
    create_ticket_search(page, public = True)

    create_ticket_search(page, public = False)

    #Create a non-admin tech user and log in
    create_tech_and_login(page)

    page.goto(f'https://{variables.subdomain}.{BASE_DOMAIN}/tickets')

    # Verify tech user can see the Public Search
    assert page.query_selector('a:has-text("Public Filter")') != None

    # Verify tech user can't see the Private Search
    assert page.query_selector('a:has-text("Private Filter")') == None
