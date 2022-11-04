import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.ticket import Ticket, wait_for_worker
from playwright.sync_api import expect
import uuid
import variables

@pytest.mark.regression
def test_ticket_deposit(page, login, api_request_context):
    # Go to Invoice Preferences page
    page.goto(f'{variables.base_url}/settings/invoices')

    # Check 'Enable the Deposits feature'
    page.check('label.checkbox input#settings_enable_deposits')
    page.click('div.mtl input[value="Save"]')
    # The form above is AJAX, Playwright won't wait for it
    page.wait_for_timeout(2000)

    # Create ticket
    ticket = Ticket(subject = 'Remote printer not working')
    ticket.create(api_request_context)
    # Make a Deposit Product
    page.goto(f'{variables.base_url}/products/new')
    page.fill('#product_name', 'Test product for Deposit')
    page.fill('textarea[name="product[description]"]', 'Test product for Deposit')
    page.fill('#product_price_retail', '10')
    page.select_option('select#category_ids', label = 'Deposit')
    page.click('#product-details >> text=Create Product')
    page.wait_for_timeout(5000)
    assert page.locator('div.alert:has-text("Product was successfully created.")').inner_text() != None

    # Go to ticket page
    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')

    # Click Actions > Take Deposit
    page.click('a.dropdown-toggle:has-text("Actions")')
    page.click('ul.dropdown-menu a.menu-default:has-text("Take Deposit")')
    page.click('li.mvs a:has-text("Test product for Deposit")')

    page.wait_for_timeout(3000)
    assert page.locator('div.alert:has-text("We created a deposit invoice")').inner_text()!= None

    page.select_option('select#payment_payment_method_id', label='Quick')

    # Click Take Payment button
    page.wait_for_timeout(5000)
    page.click('input#take-payment')

    assert page.locator('div.alert:has-text("Payment successfully applied")').inner_text() != None

    page.click('a.btn.btn-success:has-text("Continue")')

    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')
    page.click('a:has-text("Add/View Charges:")')

    page.type('#ticket_line_item_name','Labor', delay=150)
    page.click('text="Labor - Labor"')
    page.click('text=Add item to Ticket')

    # Verify that we have 'Test product for deposit' and 'Labor' line items on the page
    expect(page.locator('table.ticket-cart')).to_contain_text("Test product for Deposit")
    expect(page.locator('table.ticket-cart')).to_contain_text("Labor")

    expect(page.locator('table.ticket-cart:has-text("Test product for Deposit")')).to_contain_text('-1.0')

    page.goto(f'{variables.base_url}/tickets/{ticket.ticket_id}')

    # Make Invoice from Ticket
    page.click('form.btn-group input.btn:has-text("Make Invoice")')

    # Verify that invoice has Extended -10$
    expect(page.locator('div#line_items_table tr.line_item:has-text("Test product for Deposit")')).to_contain_text('-$10')
