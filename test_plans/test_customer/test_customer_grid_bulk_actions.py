import pytest
from fixtures.constants import *
from fixtures.login import create_account, login
from helpers.customer import Customer
from helpers.ticket import wait_for_worker
from playwright.sync_api import expect
import variables
import uuid

def test_customer_grid_bulk_actions(page, login, api_request_context):

    customer_1 = Customer(business_name = 'IService' + str(uuid.uuid4())[1:10], last_name = 'Smith')
    customer_1.create(api_request_context)

    customer_2 = Customer(business_name = 'CopyCentr' + str(uuid.uuid4())[1:10], last_name = 'Green')
    customer_2.create(api_request_context)

    page.goto(f'{variables.base_url}/customers')

    # Bulk Actions Customers > Edit
    page.click('input.selectall')
    page.click('a.bhv-bulkEdit')
    page.click('li:has-text("Edit")')
    page.wait_for_timeout(2000)

    assert page.locator('text="Bulk Edit Customers"').inner_text()
    page.select_option('select#customers_get_billing', label= 'Yes')
    page.select_option('select#customers_tax_rate_id', label = 'Default')
    page.select_option('select#customers_tax_free', label= 'No')
    page.select_option('select#customers_template_id', label ='New Template')

    # Click Update Records
    page.click('text="Update Records"')

    assert page.locator('text="We will start on that right away! (allow up to 10~ minutes)"').inner_text()


    # Go to customer1 edit page, check get billing, tax rate, tax free, Default Invoice Template fieds
    page.goto(f'{variables.base_url}/customers/{customer_1.customer_id}/edit')
    wait_for_worker(page, 'input#customer_get_billing:checked')

    expect(page.locator('select#customer_tax_rate_id')).to_contain_text('Default')
    expect(page.locator('input#customer_tax_free')).not_to_be_checked
    expect(page.locator('input#customer_get_billing')).to_be_checked
    expect(page.locator('select#customer_template_usages_attributes_2_template_id')).to_contain_text('New Template')

    # Create invoice for customer1 , check fields on invoice page
    page.goto(f'{variables.base_url}/customers/{customer_1.customer_id}')
    page.click('div.btn-group a.btn.btn-default.btn-sm:has-text("New")')
    page.click('input.menu-default[value="Invoice"]')

    expect(page.locator('div#invoice_details_widget')).not_to_contain_text('Non-Taxable Invoice')

    # Bulk Actions Customers > Edit > change tax
    page.goto(f'{variables.base_url}/customers')

    page.click('input.selectall')
    page.click('a.bhv-bulkEdit')
    page.click('li:has-text("Edit")')

    assert page.locator('text="Bulk Edit Customers"').inner_text()
    page.select_option('select#customers_tax_free', label= 'Yes')
    page.select_option('select#customers_get_billing', label= 'No')
    # Click Update Records
    page.click('text="Update Records"')


    assert page.locator('text="We will start on that right away! (allow up to 10~ minutes)"').inner_text()

    # Go to customer 2 edit page, check get billing, tax rate, tax free, Default Invoice Template fieds
    page.goto(f'{variables.base_url}/customers/{customer_2.customer_id}/edit')
    wait_for_worker(page, 'input#customer_tax_free:checked')
    expect(page.locator('input#customer_tax_free')).to_be_checked
    expect(page.locator('input#customer_get_billing')).not_to_be_checked

    # Create invoice for customer2 , check fields on invoice page
    page.goto(f'{variables.base_url}/customers/{customer_1.customer_id}')
    page.click('div.btn-group a.btn.btn-default.btn-sm:has-text("New")')
    page.click('input.menu-default[value="Invoice"]')

    page.wait_for_timeout(5000)
    expect(page.locator('div#invoice_details_widget')).to_contain_text('Non-Taxable Invoice')

    # Bulk Actions > 'Archive'
    page.goto(f'{variables.base_url}/customers')
    page.click('input.selectall')
    page.click('a.bhv-bulkEdit')

    page.click('li:has-text("Archive")')

    assert page.locator('div.modal-header:has-text("Bulk Archive Customers")').inner_text()
    # Click Archive
    page.click('input:has-text("Archive Customers")')

    # Verify that both customers were archived

    assert page.locator('text="We will start on that right away! (allow up to 10~ minutes)"').inner_text()
    page.wait_for_timeout(2000)
    page.goto(f'{variables.base_url}/customers/{customer_1.customer_id}')
    wait_for_worker(page,'text="Customer is Archived"')
    assert page.locator('text="Customer is Archived"').inner_text()

    page.goto(f'{variables.base_url}/customers/{customer_2.customer_id}')
    assert page.locator('text="Customer is Archived"').inner_text()

    # Re-enable Customer2
    page.click('text="Actions"')
    page.click('li:has-text("Re-Enable")')

    # Verify that Customer2 was reanabled
    assert page.locator('text="Customer was enabled."').inner_text()
    page.goto(f'{variables.base_url}/customers/')
    expect(page.locator('table.table-striped.borderless')).to_contain_text(customer_2.business_name)
    expect(page.locator('table.table-striped.borderless')).not_to_contain_text(customer_1.business_name)

    # Bulk Actions > Delete Customer2

    page.click('input.selectall')
    page.click('a.bhv-bulkEdit')
    page.click('li:has-text("Delete")')

    assert page.locator('text="Bulk Delete Customers"').inner_text()
    # Click Delete Customer

    page.click('text="Delete Customers"')

    assert page.locator('text="We will start on that right away! (allow up to 10~ minutes)"').inner_text()
    page.goto(f'{variables.base_url}/customers')
    wait_for_worker(page, f'text="{customer_2.business_name}"', False)
    expect(page.locator('div.main')).not_to_contain_text(customer_2.business_name)
