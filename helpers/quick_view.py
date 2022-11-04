import pytest
import re
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import create_customer
from playwright.sync_api import Page, expect
from helpers.api_token import generate_api_token
import variables

def validate_customer_quick_view(page, customer_id, url):
    quick_view_selector = (f'#quick-view-customer-{customer_id}')
    page.goto(url)
    # Wait for selector appears on the page
    page.wait_for_selector(quick_view_selector)
    # Wait for javascript event handler
    page.wait_for_timeout(5000)
    page.click(quick_view_selector)

    # Start down the list of "New" entries (Open then Close)
    page.click(f'{quick_view_selector} >> text="New"')
    page.click('text="RMM Agent Installer"')
    page.wait_for_timeout(15000)
    page.click('div:has-text("Get RMM Agent Installer") >> button')

    page.click(f'{quick_view_selector} >> text="New"')
    page.click('text="Appointment"')
    page.wait_for_timeout(5000)
    page.click('div.modal-header:has-text("New Appointment") >> button')

    page.click(f'{quick_view_selector} >> text="New"')
    page.click('a.menu-default.ajax-modalize:has-text("Reminder")')
    page.wait_for_timeout(5000)
    page.click('//*[text()="Set a new reminder"]//preceding-sibling::button/i')

    page.click(f'{quick_view_selector} >> text="New"')
    page.click('div.qv-hover a.menu-default:has-text("Email")')
    page.wait_for_timeout(500)
    page.click('div.modal-header:has-text("Compose Email") >> button')

    page.click(quick_view_selector)
    page.click(f'{quick_view_selector} >> text="New"')
    page.click('text="Invoice"')
    assert page.wait_for_selector('text=/Created successfully*/') != None
    page.goto(url)

    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)
    page.click(f'{quick_view_selector} >> text="New"')
    # For Flash messages to work properly on the next page
    # This page's users/current call must finish
    page.wait_for_timeout(5000)
    page.click('text="Estimate"')
    assert page.wait_for_selector('text=/Created successfully*/') != None
    page.goto(url)

    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)
    page.click(f'{quick_view_selector} >> text="New"')
    page.click('text="Ticket"')
    page.wait_for_timeout(500)
    expect(page.locator('.customer-title')).to_contain_text('New Ticket for')
    page.goto(url)

    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)
    page.click(f'{quick_view_selector} >> text="New"')
    page.click('text="Payment"')
    expect(page.locator('.customer-title')).to_contain_text('New Payment')
    page.goto(url)

    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)
    page.click(f'{quick_view_selector} >> text="New"')
    # For Flash messages to work properly on the next page
    # This page's users/current call must finish
    page.wait_for_timeout(5000)
    page.click('text="Customer Purchase"')
    assert page.wait_for_selector('text=/Customer purchase was successfully created.*/') != None
    page.goto(url)

    page.wait_for_selector(quick_view_selector)
    page.wait_for_timeout(3000)
    page.click(quick_view_selector)
    page.click(f'{quick_view_selector} >> text="New"')
    page.click('text="Recurring Invoice"')
    expect(page.locator('.customer-title')).to_contain_text('New Recurring Invoice')
    page.goto(url)
